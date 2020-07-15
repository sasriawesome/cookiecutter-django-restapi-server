$(function () {
  $('#sidenav').metisMenu();

  menuToggle = function() {
    var sidenav = $('#sidenav');
    var overlay = $('#overlay');
    var active = $('#sidenav').hasClass('active');
    if (active != true) {
      sidenav.addClass('active');
      overlay.addClass('active');
    } else {
      sidenav.removeClass('active');
      overlay.removeClass('active');
    }
  }

  $('#sidenavButton').on('click', function(event){
    menuToggle();
  })
  $('#overlay').on('click', function(event){
    menuToggle();
  })
});