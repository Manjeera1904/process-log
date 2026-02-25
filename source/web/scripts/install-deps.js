const fs = require('node:fs')
const { execSync } = require('node:child_process')
const path = require('node:path')

const libPkgPath = path.resolve(__dirname, '../package.json')
const libPkg = JSON.parse(fs.readFileSync(libPkgPath, 'utf8'))

const peerDeps = libPkg.peerDependencies || {}
const deps = Object.entries(peerDeps).map(
  ([name, version]) => `${name}@${version}`,
)

if (deps.length) {
  console.log(`Installing peer dependencies: ${deps.join(' ')}`)
  execSync(`pnpm install ${deps.join(' ')}`, { stdio: 'inherit' })
}
else {
  console.log('No peerDependencies found.')
}

const dependencies = libPkg.dependencies || {}
const actualDependencies = Object.entries(dependencies).map(
  ([name, version]) => `${name}@${version}`,
)

if (actualDependencies.length) {
  console.log(
    `Installing Actual dependencies: ${actualDependencies.join(' ')}`,
  )
  execSync(`pnpm install ${actualDependencies.join(' ')}`, {
    stdio: 'inherit',
  })
}
else {
  console.log('No actualDependencies found.')
}

const devDependencies = libPkg.devDependencies || {}
const actualDevDependencies = Object.entries(devDependencies).map(
  ([name, version]) => `${name}@${version}`,
)

if (actualDevDependencies.length) {
  console.log(
    `Installing Actual Dev dependencies: ${actualDevDependencies.join(' ')}`,
  )
  execSync(`pnpm install -D ${actualDevDependencies.join(' ')}`, {
    stdio: 'inherit',
  })
}
else {
  console.log('No actualDevDependencies found.')
}
