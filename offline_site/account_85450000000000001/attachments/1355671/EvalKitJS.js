/*EvaluationKIT START*/var evalkit_jshosted = document.createElement('script');evalkit_jshosted.setAttribute('defer', 'defer');evalkit_jshosted.setAttribute('type', 'text/javascript');evalkit_jshosted.setAttribute('src', 'https://etbu.evaluationkit.com/canvas/js');document.getElementsByTagName('head')[0].appendChild(evalkit_jshosted);/*EvaluationKIT END*/

//
// Modified: Sat Aug 24 17:07:08 2019 -0500 sp 08.04.2021
//

// Adds help link to main login dialog
$('.ic-Login__forgot').append('<a class="first_time_link" href="https://www.etbu.edu/about-etbu/faq/canvas-faqs" target="_blank">First Time Signing In?</a>');

// Adds help link to mobile login dialog
$('.forgotBlock').append('<br/><a href="https://www.etbu.edu/about-etbu/faq/canvas-faqs" target="_blank">First Time Signing In?</a>');
$('.forgotBlock').append('<br/><a class="email_change" href="https://passwordreset.microsoftonline.com" target="_blank">Change ETBU Password Here</a>');
$('.forgotBlock').append('<div class="login_info"><b>Login Issues?</b><br/>Your canvas password is linked to your email password.<br/>Your username is just the first part of your email address.<br/></div>');
//Adds Email Password Change to main login dialog
$('.ic-Login__forgot').append('<br/><a class="email_change" href="https://passwordreset.microsoftonline.com" target="_blank">Change ETBU Password Here</a>');

// Adds Login Help Information to main login dialog
$('.ic-Login__body').append('<div class="login_info"><b>Login Issues?</b><br/>Your canvas password is linked to your email password.<br/>Your username is just the first part of your email address.<br/></div>');


// Adds "@etbu.edu" to user name input control and sets wrapper focus
$(document).ready(function() {
  var etbu_login_mod  = '<div class="ic-Form-control ic-Form-control--login">';
      etbu_login_mod += '  <div class="etbu-control-wrapper">';
      etbu_login_mod += '    <input class="etbu-username ic-Input text" type="text" name="pseudonym_session[unique_id]" id="pseudonym_session_unique_id">';
      etbu_login_mod += '    <div class="etbu-domain">@etbu.edu</div>';
      etbu_login_mod += '  </div>';
      etbu_login_mod += '</div>';

  $("input[type='text'][name='pseudonym_session[unique_id]']").replaceWith(etbu_login_mod);

  $('#pseudonym_session_unique_id').on('focus', function() {
    $('.etbu-control-wrapper').addClass('etbu-pseudo-focus');
  });

  $('#pseudonym_session_unique_id').on('blur', function() {
    $('.etbu-control-wrapper').removeClass('etbu-pseudo-focus');
  });

  $('#pseudonym_session_unique_id').focus();
});