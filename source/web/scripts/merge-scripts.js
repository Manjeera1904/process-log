const fs = require('node:fs')
const path = require('node:path')

const libPkgPath = path.resolve(__dirname, '../package.json')
const appPkgPath = path.resolve(__dirname, '../../../package.json')

const libPkg = JSON.parse(fs.readFileSync(libPkgPath, 'utf8'))
const appPkg = JSON.parse(fs.readFileSync(appPkgPath, 'utf8'))

const mergedScripts = {
  ...libPkg.scripts,
  ...appPkg.scripts, // app overrides take precedence
}

appPkg.scripts = mergedScripts

fs.writeFileSync(appPkgPath, JSON.stringify(appPkg, null, 2))
