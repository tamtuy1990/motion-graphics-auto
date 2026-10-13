import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

import { checkRendererReleases } from './version-check.js'

const packageDir = dirname(fileURLToPath(import.meta.url))
const skillDir = join(packageDir, 'skills', 'motion-graphics-auto')
const skillFile = join(skillDir, 'SKILL.md')
const skillSource = readFileSync(skillFile, 'utf8')
const frontmatterMatch = skillSource.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/u)

if (!frontmatterMatch) {
  throw new Error(`Missing YAML frontmatter in ${skillFile}`)
}

function readScalar(key) {
  const match = frontmatterMatch[1].match(new RegExp(`^${key}:\\s*(.*?)\\s*$`, 'mu'))
  if (!match) return undefined
  const value = match[1]
  if (value.length >= 2 && value[0] === '"' && value.at(-1) === '"') return value.slice(1, -1)
  if (value.length >= 2 && value[0] === "'" && value.at(-1) === "'") return value.slice(1, -1)
  return value
}

const skillName = readScalar('name')
const skillDescription = readScalar('description')
const skillWhenToUse = readScalar('whenToUse')
const skillContent = skillSource.slice(frontmatterMatch[0].length).trimStart()

if (skillName !== 'motion-graphics-auto' || !skillDescription || !skillContent) {
  throw new Error('The packaged skill must define name, description, and a non-empty body.')
}

export const name = 'dsh-motion-graphics-auto'
export const inject = ['skills', 'tools']

export function apply(ctx) {
  if (typeof ctx.skills?.register !== 'function' || typeof ctx.tools?.register !== 'function') {
    throw new Error('dsh-motion-graphics-auto requires the DeepSeek Harness skills and tools services.')
  }

  ctx.effect(() => {
    const disposeSkill = ctx.skills.register({
      name: skillName,
      description: skillDescription,
      source: 'runtime',
      ...(skillWhenToUse ? { whenToUse: skillWhenToUse } : {}),
      content: skillContent,
      resourceBase: { kind: 'directory', path: skillDir },
      invocation: { modelInvocable: true, userInvocable: true },
    })

    const disposeTool = ctx.tools.register({
      name: 'motion_graphics_auto_check_releases',
      description: 'Check GitHub latest stable releases for Remotion and HyperFrames once per Asia/Ho_Chi_Minh calendar day. Uses the persistent DSH_HOME cache and does not call a language model.',
      parameters: {
        type: 'object',
        properties: {},
        required: [],
        additionalProperties: false,
      },
      output: {
        schema: { type: 'string' },
        render: (_args, value) => [{ type: 'text', text: value }],
      },
      async execute(_args, exec) {
        const result = await checkRendererReleases({ signal: exec.signal })
        return JSON.stringify(result, null, 2)
      },
    })

    return () => {
      disposeTool()
      disposeSkill()
    }
  })
}
