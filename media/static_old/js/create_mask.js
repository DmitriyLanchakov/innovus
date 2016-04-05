function CreateTextMask(elementid, masktext){
            var element = $("."+elementid);
            element.val(masktext);

            element.focus(function(){
                if (element.val() == masktext){
                    element.val("");
                }
            })

            element.blur(function(){
                if (element.val().length == 0){
                    element.val(masktext);
                }
            })
        }
$(function(){
  var search_text = "Поиск";
  var login_text = "E-mail";
  var password_text = "Пароль";
  if ($("body").hasClass("en")) {
    search_text = "Search";
    password_text = "Password";
  }
  CreateTextMask("search_input", search_text);
  CreateTextMask("login_t", login_text);
  CreateTextMask("password_t", password_text);
})
