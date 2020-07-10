$(document).ready(function () {
    $('#contact form').on('submit', function (e) {
        e.preventDefault();
        var regex = /^([a-zA-Z0-9_.+-])+@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        var $form = $(e.currentTarget),
            $email = $form.find('#id_email'), $button = $form.find('button[type=submit]');
        if (!regex.test($email.val())) {
            vaca = $email.closest('form-group')
            $email.closest('.form-group').addClass('text-danger');
        } else {
            $form.find('.form-group').addClass('is-valid').removeClass('text-danger');
            $('#ContactModal').modal('hide');
            $form[0].submit();
        }
    });
});