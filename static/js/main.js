function sendMessage(){
    $('.chat_screen').append('<p id="user_mesg"><span>'+$( "#messageInput" ).val()+'</span></p>');
    $.ajax({
        type:'POST',
        url:'/chat_message',
        data:{
            message:$('#messageInput').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(response){
            $('.chat_screen').append('<p id="bot_mesg"><span>'+response+'</span></p>'); 
            $('#messageInput').val('');
        }
    });
};


function advocate_update_profile(){
    $.ajax({
        type:'POST',
        url:'/advocate/update_profile',
        data:{
            f_name:$('#f_name').val(),
            l_name:$('#l_name').val(),
            email:$('#email').val(),
            phone:$("#contact").intlTelInput("getNumber"),
            dob:$('#dob').val(),
            expertise:$('#expertise').val(),
            experience:$('#experience').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(response){
            if(response['status'] == 'success'){
                alert('Profile updated successfully');
            }
            else{
                alert('Error updating profile');
            }
        }
    });
}