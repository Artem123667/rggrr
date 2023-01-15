const { series, parallel, src, pipe, dest} = require('gulp');
const concat = require('gulp-concat');
const cleanCSS = require('gulp-clean-css');
const remove = require('gulp-clean');
const postcss = require('gulp-postcss');
// const rsync = require('gulp-rsync');  !!! ПОСМОТРЕТЬ ВИДОС
const gutil = require('gulp-util');
const ftp = require('vinyl-ftp');
const watch = require('gulp-watch');

/** Configuration **/
var user = 'n91632yo_total'
var password = '6A*cAQGr'
var host = 'n91632yo.beget.tech'
var port = 21
var localFilesGlob = ['img/**/*', 'fonts/**/*', 'dist/**/*', 'index.html']
var remoteFolder = '/portfolio'

function clean(cb) {
  return src('dist/**', {read: false})
        .pipe(remove());
}
function cleanTemp(cb) {
  return src('./css/vendors/min', {read: false})
        .pipe(remove());
}

function cssTranspile(cb) {
   return src('./css/*.css')
        .pipe(postcss())
        .pipe(dest('./dist'));
}
function cssVendorsMinify(cb) {
  // body omitted
 return src('./css/vendors/*.css')
    .pipe(cleanCSS('*.css'))
    .pipe(dest('./css/vendors/min/'));
}
function cssVendorsBundle(cb) {
  // body omitted
  return src('./css/vendors/min/*.css')
    .pipe(concat('vendors.min.css'))
    .pipe(dest('./dist/')); 
}
function jsTranspile(cb) {
  // body omitted
  cb();
}

function jsBundle(cb) {
  // body omitted
  return src('./js/*.js')
    .pipe(concat('all.js'))
    .pipe(dest('./dist/')); 
}

function jsMinify(cb) {
  // body omitted
  cb();
}

function publish(cb) {
  var conn = getFtpConnection()

  return src(localFilesGlob, { base: '.', buffer: false })
    .pipe(conn.newer(remoteFolder)) // only upload newer files
    .pipe(conn.dest(remoteFolder))
}

function watcher() {
  var conn = getFtpConnection()

  watch(localFilesGlob).on('change', function(event) {
    console.log(
      'Changes detected! Uploading file "' + event.path + '", ' + event.type
    )

    return src([event.path], { base: '.', buffer: false })
      .pipe(conn.newer(remoteFolder)) // only upload newer files
      .pipe(conn.dest(remoteFolder))
  })
}

function getFtpConnection() {
  return ftp.create({
    host: host,
    port: port,
    user: user,
    password: password,
    parallel: 5,
    log: gutil.log,
  })
}

exports.publish = publish;

exports.watcher = watcher;

exports.default = series(
  clean,
  jsTranspile,
  jsBundle,
  cssTranspile,
  cssVendorsMinify,
  cssVendorsBundle,
  // parallel(cssMinify, jsMinify),
  cleanTemp,
  publish
);