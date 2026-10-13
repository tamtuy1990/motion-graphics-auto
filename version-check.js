import { randomUUID } from 'node:crypto'
import { mkdir, open, readFile, rename, stat, unlink, writeFile } from 'node:fs/promises'
import { homedir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

export const RELEASE_TIME_ZONE = 'Asia/Ho_Chi_Minh'

const projects = [
  { key: 'remotion', repository: 'remotion-dev/remotion' },
  { key: 'hyperframes', repository: 'heygen-com/hyperframes' },
]

const bundledCachePath = fileURLToPath(new URL(
  './skills/motion-graphics-auto/references/github-release-cache.json',
  import.meta.url,
))

function localDate(now) {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: RELEASE_TIME_ZONE,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(now)
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]))
  return `${values.year}-${values.month}-${values.day}`
}

function isDailyCache(value, date) {
  if (!value || value.checked_date !== date || value.timezone !== RELEASE_TIME_ZONE ||
      !value.projects || typeof value.projects !== 'object') return false
  return projects.every(({ key }) => {
    const project = value.projects[key]
    return project && typeof project === 'object' && typeof project.repository === 'string' &&
      (typeof project.tag === 'string' || ['pending', 'ok', 'error'].includes(project.status))
  })
}

async function readJson(path) {
  try {
    return JSON.parse(await readFile(path, 'utf8'))
  } catch (error) {
    if (error?.code === 'ENOENT') return undefined
    return undefined
  }
}

async function writeAtomic(path, value) {
  const temporaryPath = `${path}.${process.pid}.${randomUUID()}.tmp`
  await writeFile(temporaryPath, `${JSON.stringify(value, null, 2)}\n`, { encoding: 'utf8', mode: 0o600 })
  await rename(temporaryPath, path)
}

function publicResult(cache, status) {
  return { ...cache, status, cache_scope: 'DSH_HOME shared daily cache' }
}

async function delay(ms, signal) {
  if (signal?.aborted) throw signal.reason ?? new Error('Cancelled')
  await new Promise((resolve, reject) => {
    const timer = setTimeout(done, ms)
    function done() {
      signal?.removeEventListener('abort', abort)
      resolve()
    }
    function abort() {
      clearTimeout(timer)
      signal?.removeEventListener('abort', abort)
      reject(signal.reason ?? new Error('Cancelled'))
    }
    signal?.addEventListener('abort', abort, { once: true })
  })
}

async function acquireLock(lockPath, date, cachePath, signal) {
  const deadline = Date.now() + 20_000
  while (true) {
    if (signal?.aborted) throw signal.reason ?? new Error('Cancelled')
    try {
      return await open(lockPath, 'wx', 0o600)
    } catch (error) {
      if (error?.code !== 'EEXIST') throw error
    }

    const current = await readJson(cachePath)
    if (isDailyCache(current, date)) return undefined

    try {
      const lockStat = await stat(lockPath)
      if (Date.now() - lockStat.mtimeMs > 60_000) {
        try {
          await unlink(lockPath)
          continue
        } catch (error) {
          if (error?.code !== 'ENOENT') throw error
        }
      }
    } catch (error) {
      if (error?.code !== 'ENOENT') throw error
    }

    if (Date.now() >= deadline) return undefined
    await delay(250, signal)
  }
}

async function fetchRelease(repository, { fetchImpl, signal, timeoutMs }) {
  const controller = new AbortController()
  const forwardAbort = () => controller.abort(signal.reason ?? new Error('Cancelled'))
  if (signal?.aborted) forwardAbort()
  else signal?.addEventListener('abort', forwardAbort, { once: true })
  const timer = setTimeout(() => controller.abort(new Error('GitHub request timed out')), timeoutMs)

  try {
    const response = await fetchImpl(`https://api.github.com/repos/${repository}/releases/latest`, {
      headers: {
        accept: 'application/vnd.github+json',
        'user-agent': 'dsh-motion-graphics-auto/0.1.0',
        'x-github-api-version': '2022-11-28',
      },
      signal: controller.signal,
    })
    if (!response.ok) throw new Error(`GitHub returned HTTP ${response.status}`)
    const release = await response.json()
    if (typeof release?.tag_name !== 'string' || typeof release?.html_url !== 'string') {
      throw new Error('GitHub latest-release response is missing tag_name or html_url')
    }
    return {
      status: 'ok',
      repository,
      tag: release.tag_name,
      release_url: release.html_url,
      ...(typeof release.published_at === 'string' ? { published_at: release.published_at } : {}),
      prerelease: Boolean(release.prerelease),
    }
  } catch (error) {
    return {
      status: 'error',
      repository,
      message: String(error?.message ?? error).slice(0, 300),
    }
  } finally {
    clearTimeout(timer)
    signal?.removeEventListener('abort', forwardAbort)
  }
}

function cacheStatus(cache) {
  if (cache.status === 'checking') return 'check_incomplete'
  if (cache.projects && Object.values(cache.projects).some(project => project?.status === 'error')) return 'partial'
  return 'checked'
}

/**
 * Check both official GitHub latest-stable-release endpoints at most once per local date.
 * Failures are cached for the day too, so repeated calls do not become hidden retries.
 */
export async function checkRendererReleases({
  dshHome = process.env.DSH_HOME || join(homedir(), '.dsh'),
  now = new Date(),
  fetchImpl = globalThis.fetch,
  signal,
  timeoutMs = 12_000,
} = {}) {
  const date = localDate(now)
  const cachePath = join(dshHome, 'cache', 'motion-graphics-auto', 'github-release-cache.json')
  const lockPath = `${cachePath}.lock`

  const cached = await readJson(cachePath)
  if (isDailyCache(cached, date)) {
    return publicResult(cached, cached.status === 'checking' ? 'check_incomplete' : 'cached')
  }

  const packaged = await readJson(bundledCachePath)
  if (isDailyCache(packaged, date)) {
    try {
      await mkdir(dirname(cachePath), { recursive: true })
      await writeAtomic(cachePath, packaged)
    } catch {
      // The signed-off package snapshot is still valid for this date; avoid duplicate network checks.
    }
    return publicResult(packaged, 'cached_from_plugin_package')
  }

  if (typeof fetchImpl !== 'function') {
    return { status: 'not_checked', checked_date: date, timezone: RELEASE_TIME_ZONE, message: 'Fetch is unavailable in this Node runtime.' }
  }

  try {
    await mkdir(dirname(cachePath), { recursive: true })
  } catch (error) {
    return {
      status: 'not_checked_cache_unavailable',
      checked_date: date,
      timezone: RELEASE_TIME_ZONE,
      message: `Cannot create the persistent DSH_HOME cache: ${String(error?.message ?? error).slice(0, 200)}`,
    }
  }

  let lock
  try {
    lock = await acquireLock(lockPath, date, cachePath, signal)
  } catch (error) {
    return { status: 'not_checked', checked_date: date, timezone: RELEASE_TIME_ZONE, message: String(error?.message ?? error).slice(0, 300) }
  }

  if (!lock) {
    const concurrentCache = await readJson(cachePath)
    if (isDailyCache(concurrentCache, date)) {
      return publicResult(concurrentCache, concurrentCache.status === 'checking' ? 'check_incomplete' : 'cached')
    }
    return {
      status: 'check_in_progress',
      checked_date: date,
      timezone: RELEASE_TIME_ZONE,
      message: 'Another process owns today’s GitHub check lock; no duplicate requests were sent.',
    }
  }

  try {
    const latestCache = await readJson(cachePath)
    if (isDailyCache(latestCache, date)) {
      return publicResult(latestCache, latestCache.status === 'checking' ? 'check_incomplete' : 'cached')
    }

    const checking = {
      checked_date: date,
      timezone: RELEASE_TIME_ZONE,
      source: 'GitHub latest stable Releases API',
      status: 'checking',
      projects: Object.fromEntries(projects.map(project => [project.key, { status: 'pending', repository: project.repository }])),
    }
    try {
      await writeAtomic(cachePath, checking)
    } catch (error) {
      return {
        status: 'not_checked_cache_unavailable',
        checked_date: date,
        timezone: RELEASE_TIME_ZONE,
        message: `Cannot persist the daily-check marker; no GitHub requests were sent: ${String(error?.message ?? error).slice(0, 200)}`,
      }
    }

    const results = await Promise.all(projects.map(async project => [
      project.key,
      await fetchRelease(project.repository, { fetchImpl, signal, timeoutMs }),
    ]))
    const result = {
      checked_date: date,
      timezone: RELEASE_TIME_ZONE,
      source: 'GitHub latest stable Releases API',
      status: 'complete',
      projects: Object.fromEntries(results),
    }

    try {
      await writeAtomic(cachePath, result)
    } catch (error) {
      return {
        ...result,
        status: 'checked_but_cache_write_failed',
        cache_error: String(error?.message ?? error).slice(0, 200),
        message: 'Do not retry today; two requests were already sent. The daily marker may not survive a restart.',
      }
    }
    return publicResult(result, cacheStatus(result))
  } finally {
    try {
      await lock.close()
    } finally {
      try {
        await unlink(lockPath)
      } catch (error) {
        if (error?.code !== 'ENOENT') throw error
      }
    }
  }
}
