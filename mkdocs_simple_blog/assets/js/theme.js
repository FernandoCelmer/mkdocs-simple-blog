document.addEventListener("DOMContentLoaded", function(){
    if (window.innerWidth < 992) {
    
      document.querySelectorAll('.navbar .dropdown').forEach(function(everydropdown){
        everydropdown.addEventListener('hidden.bs.dropdown', function () {
            this.querySelectorAll('.submenu').forEach(function(everysubmenu){
              everysubmenu.style.display = 'none';
            });
        })
      });
    
      document.querySelectorAll('.dropdown-menu a').forEach(function(element){
        element.addEventListener('click', function (e) {
            let nextEl = this.nextElementSibling;
            if(nextEl && nextEl.classList.contains('submenu')) {	
              e.preventDefault();
              if(nextEl.style.display == 'block'){
                nextEl.style.display = 'none';
              } else {
                nextEl.style.display = 'block';
              }
    
            }
        });
      })
    }

    const themes = {
      dark: {
        '--text': 'white',
        '--title': 'white',
        '--primary': 'white',
        '--background': 'black'
      },
      light: {
        '--text': 'black',
        '--title': 'black',
        '--primary': 'black',
        '--background': 'white'
      }
    };

    [...document.querySelectorAll('.color-button')].forEach(el => {
        el.addEventListener('click', () => {
            const theme = themes[el.dataset.theme];
            for (var variable in theme) {
                document.documentElement.style.setProperty(variable, theme[variable]);
            };
        });
    });

    var buttons = document.querySelectorAll("button[color-primary]")
    buttons.forEach(function(button) {
      button.addEventListener("click", function() {
          var attr = this.getAttribute("color-primary")
          document.documentElement.style.setProperty('--primary', attr);
      })
    })

    var buttons = document.querySelectorAll("button[color-text]")
    buttons.forEach(function(button) {
      button.addEventListener("click", function() {
          var attr = this.getAttribute("color-text")
          document.documentElement.style.setProperty('--text', attr);
      })
    })

    var buttons = document.querySelectorAll("button[color-title]")
    buttons.forEach(function(button) {
      button.addEventListener("click", function() {
          var attr = this.getAttribute("color-title")
          document.documentElement.style.setProperty('--title', attr);
      })
    })

    var buttons = document.querySelectorAll("button[color-background]")
    buttons.forEach(function(button) {
      button.addEventListener("click", function() {
          var attr = this.getAttribute("color-background")
          document.documentElement.style.setProperty('--background', attr);
      })
    })

    var buttons = document.querySelectorAll("button[format-text]")
    buttons.forEach(function(button) {
      button.addEventListener("click", function() {
          var attr = this.getAttribute("format-text")
          title = document.getElementById("title").classList;
          title.remove("bold")
          title.remove("italic")
          title.remove("scratched")
          title.remove("underline")
          title.remove("overline")
          title.add(attr);
      })
    })



    
});


