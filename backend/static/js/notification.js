const message_list= document.querySelectorAll('.messages-container > a')



message_list.forEach((item) => {
    item.addEventListener('click', function(){
        const nftID= this.id
        $.ajax({
                type: 'POST',
                url: `/accounts/notifications-update/`,
                data:{
                    nftID: nftID,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(response) {
                    if (response.status === 'ok') {
                      //read
                      console.log(`${response.id}`);
                    }else {
                      //pass
                      console.log(`${response.id}`);
                    }
                  },
                error: function(response) {
                  alert('An error occurred');
                }
              });
    })
})