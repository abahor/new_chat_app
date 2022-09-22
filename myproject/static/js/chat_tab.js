$(document).ready(function() {

    var socket = io();


    $('#btn-chat').on('click', function () {
        socket.emit('send_message',{'text': $('#btn-input').val() })
    });

    socket.on('new_message', function(msg) {

        console.log('Received message');
        console.log(msg);
        if( $('#user').val() == msg['sender'] ){
        console.log('s')

        var d = document.getElementById('sent-template').content;
        var copyHTML = document.importNode(d , true);
        copyHTML.querySelector('.subject').textContent = msg['text']['text'];

         $('#panel-body').append(
             copyHTML
        );

        } else {

        var d = document.getElementById('receive-template').content;
        var copyHTML = document.importNode(d , true);
        copyHTML.querySelector('.subject').textContent = msg['text']['text'];
         console.log('sad')
         $('#panel-body').append(
             copyHTML
        );


        }


    }
    );

    }
    );
