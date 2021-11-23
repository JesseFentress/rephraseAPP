
var popup = document.getElementById('popup_btn');

   popup.addEventListener('click', function() {

      document.querySelector('.popup').style.display = 'flex';
   });

var close = document.getElementById('close');

   close.addEventListener('click', function() {

      document.querySelector('.popup').style.display = 'none';
   });

   var chatpopup = document.getElementById('create_chat_btn');

   chatpopup.addEventListener('click', function() {

      document.querySelector('.popup').style.display = 'flex';
   });


