document.addEventListener("DOMContentLoaded", function () {
  let t = {
    dark: {
      "--text": "white",
      "--title": "white",
      "--primary": "white",
      "--background": "black",
    },
    light: {
      "--text": "black",
      "--title": "black",
      "--primary": "black",
      "--background": "white",
    },
  };
  [...document.querySelectorAll(".color-button")].forEach((e) => {
    e.addEventListener("click", () => {
      let n = t[e.dataset.theme];
      for (var r in n) document.documentElement.style.setProperty(r, n[r]);
    });
  });

  var e = document.querySelectorAll("button[color-primary]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("color-primary");
      document.documentElement.style.setProperty("--primary", t);
    });
  });

  var e = document.querySelectorAll("button[color-text]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("color-text");
      document.documentElement.style.setProperty("--text", t);
    });
  });

  var e = document.querySelectorAll("button[color-title]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("color-title");
      document.documentElement.style.setProperty("--title", t);
    });
  });

  var e = document.querySelectorAll("button[color-background]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("color-background");
      document.documentElement.style.setProperty("--background", t);
    });
  });

  var e = document.querySelectorAll("button[style-site-name]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("style-site-name");
      (title = document.getElementById("component-site-name").classList).remove(
        "bold"
      ),
        title.remove("italic"),
        title.remove("scratched"),
        title.remove("underline"),
        title.remove("overline"),
        title.add(t);
    });
  });

  var e = document.querySelectorAll("button[style-title]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("style-title");
      (title = document.getElementById("component-title").classList).remove(
        "bold"
      ),
        title.remove("italic"),
        title.remove("scratched"),
        title.remove("underline"),
        title.remove("overline"),
        title.add(t);
    });
  });

  var e = document.querySelectorAll("button[component-id]");
  e.forEach(function (t) {
    t.addEventListener("click", function () {
      var t = this.getAttribute("component-id"),
        e = this.getAttribute("status");
      document.getElementById(t).hidden = JSON.parse(e);
    });
  });

  var sidebarTrue = document.getElementById("sidebar-true");
  if (sidebarTrue) {
    sidebarTrue.addEventListener("click", function () {
      var sidebar = document.getElementById("component-sidebar");
      var content = document.getElementById("component-content");
      if (sidebar) {
        sidebar.style.display = "";
        sidebar.classList.remove("d-none");
        sidebar.classList.add("d-md-block", "col-md-3");
        sidebar.classList.remove("col-0");
      }
      if (content) {
        content.classList.remove("col-12");
        content.classList.add("col-md-9");
      }
    });
  }

  var sidebarFalse = document.getElementById("sidebar-false");
  if (sidebarFalse) {
    sidebarFalse.addEventListener("click", function () {
      var sidebar = document.getElementById("component-sidebar");
      var content = document.getElementById("component-content");
      if (sidebar) {
        sidebar.style.display = "none";
        sidebar.classList.add("d-none");
        sidebar.classList.remove("d-md-block", "col-md-3");
      }
      if (content) {
        content.classList.remove("col-md-9");
        content.classList.add("col-12");
      }
    });
  }
});
