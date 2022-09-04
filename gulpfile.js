const fs = require("fs");
const path = require("path");
const gulp = require("gulp");
const include = require("gulp-include");
const handlebars = require("gulp-hb");
const sass = require("gulp-sass")(require("sass"));
const rename = require("gulp-rename");

const BUILDDIR = "./build/";

function render_css(resolve) {
  gulp
    .src("./src/css/*.scss")
    .pipe(sass({ includePaths: ["css"] }))
    .pipe(gulp.dest(BUILDDIR));
  resolve();
}

function compile_page(resolve) {
  gulp
    .src(path.join("./src/views/index.hbs"))
    .pipe(include({ includePaths: ["/svg"] }))

    .pipe(
      handlebars({ encoding: "utf8", debug: true, bustCache: true }).partials("./views/[!index]*.hbs").partials("./views/popups/*.hbs").partials("./views/components/*.hbs").helpers("./helpers/**/*.js").data({
        projectSlug: "image-tools",
        title: "Image Tools",
        layout: false,
      })
    )
    .pipe(rename("index.html"))
    .pipe(gulp.dest(BUILDDIR));
  resolve();
}

try {
  fs.rmdirSync(BUILDDIR, { recursive: true });
  fs.mkdirSync(BUILDDIR);
} catch (err) {
  console.log("failed to find build folder, but it's probably fine");
}

function defaultTask(cb) {
  gulp.parallel(render_css, compile_page)();
  cb();
}

exports.default = defaultTask;
