import assert from 'node:assert/strict'
import { mkdtemp, readFile, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import test from 'node:test'

import { apply, inject, name } from '../index.js'
import { checkRendererReleases } from '../version-check.js'

test('plugin registers an invocable skill, its packaged resources, and a fixed-schema release tool', () => {
  const skills = []
  const tools = []
  const cleanups = []
  const ctx = {
    skills: { register(value) { skills.push(value); return () => cleanups.push('skill') } },
    tools: { register(value) { tools.push(value); return () => cleanups.push('tool') } },
    effect(callback) { cleanups.push(callback()) },
  }

  assert.equal(name, 'dsh-motion-graphics-auto')
  assert.deepEqual(inject, ['skills', 'tools'])
  apply(ctx)

  assert.equal(skills.length, 1)
  assert.equal(skills[0].name, 'motion-graphics-auto')
  assert.equal(skills[0].source, 'runtime')
  assert.equal(skills[0].invocation.modelInvocable, true)
  assert.equal(skills[0].invocation.userInvocable, true)
  assert.match(skills[0].content, /one planning request by default/iu)
  assert.equal(skills[0].resourceBase.kind, 'directory')

  assert.equal(tools.length, 1)
  assert.equal(tools[0].name, 'motion_graphics_auto_check_releases')
  assert.deepEqual(tools[0].parameters, {
    type: 'object',
    properties: {},
    required: [],
    additionalProperties: false,
  })
  assert.equal(tools[0].output.schema.type, 'string')
  assert.equal(typeof tools[0].execute, 'function')
  assert.equal(typeof cleanups[0], 'function')
})

test('daily release check fetches both GitHub endpoints once and then uses persistent cache', async () => {
  const dshHome = await mkdtemp(join(tmpdir(), 'dsh-motion-graphics-auto-'))
  const calls = []
  const fetchImpl = async (url) => {
    calls.push(url)
    const repository = url.includes('remotion-dev') ? 'remotion-dev/remotion' : 'heygen-com/hyperframes'
    const tag = repository.startsWith('remotion') ? 'v4.0.535' : 'v0.8.150'
    return new Response(JSON.stringify({
      tag_name: tag,
      html_url: `https://github.com/${repository}/releases/tag/${tag}`,
      published_at: '2026-10-13T00:00:00Z',
      prerelease: false,
    }), { status: 200, headers: { 'content-type': 'application/json' } })
  }

  try {
    const now = new Date('2026-10-14T08:00:00Z')
    const first = await checkRendererReleases({ dshHome, now, fetchImpl })
    assert.equal(first.status, 'checked')
    assert.equal(calls.length, 2)
    assert.equal(first.projects.remotion.tag, 'v4.0.535')
    assert.equal(first.projects.hyperframes.tag, 'v0.8.150')

    const second = await checkRendererReleases({ dshHome, now, fetchImpl })
    assert.equal(second.status, 'cached')
    assert.equal(calls.length, 2)

    const cache = JSON.parse(await readFile(join(dshHome, 'cache/motion-graphics-auto/github-release-cache.json'), 'utf8'))
    assert.equal(cache.checked_date, '2026-10-14')
  } finally {
    await rm(dshHome, { recursive: true, force: true })
  }
})
