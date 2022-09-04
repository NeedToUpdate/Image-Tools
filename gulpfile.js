const fs = require("fs");
const path = require("path");
const gulp = require("gulp");
const include = require("gulp-include");
const handlebars = require("gulp-hb");
const sass = require("gulp-sass")(require("sass"));
const rename = require("gulp-rename");
const sourcemaps = require("gulp-sourcemaps");
const babel = require("gulp-babel");
const concat = require("gulp-concat");
const uglify = require("gulp-uglify");
const minify = require("gulp-minifier");
const watch = require("gulp-watch");

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
    .pipe(
      handlebars({ encoding: "utf8", debug: true, bustCache: true })
        .partials("./src/views/[!index]*.hbs")
        .partials("./src/views/components/*.hbs")
        .helpers("./src/helpers/**/*.js")
        .data({
          projectSlug: "image-tools",
          title: "Image Tools",
          layout: false,
        })
        .data("./src/data/**/*.{js,json}")
    )
    .pipe(rename("index.html"))
    .pipe(gulp.dest(BUILDDIR));
  resolve();
}

function combine_js(resolve) {
  gulp
    .src("src/js/**/*.js")
    .pipe(sourcemaps.init())
    .pipe(
      babel({
        presets: ["@babel/env"],
      })
    )
    .pipe(concat("script.js"))
    .pipe(uglify())
    .pipe(
      minify({
        minify: true,
        minifyJS: {
          sourceMap: true,
        },
      })
    )
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest(BUILDDIR));
  resolve();
}

function clear(resolve) {
  try {
    fs.rmdirSync(BUILDDIR, { recursive: true });
    fs.mkdirSync(BUILDDIR);
  } catch (err) {
    console.log("failed to find build folder, but it's probably fine");
  }
  resolve();
}

function defaultTask(cb) {
  gulp.series(clear, gulp.parallel(render_css, compile_page, combine_js))();
  cb();
}

gulp.task("watch", function () {
  gulp.watch("./src/**/*", defaultTask);
});

exports.default = defaultTask;
