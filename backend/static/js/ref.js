// const selectBtns= document.querySelectorAll('.lower button')
// const giftID= document.querySelector('input[name="gift-id"]')

// selectBtns.forEach(x => {
//     x.addEventListener('click', function(){
//         const reciver= this.id
//         selectBtns.forEach(btn => {
//             btn.setAttribute('disabled', '')
//         })
//         $.ajax({
//             type: 'POST',
//             url: `/ref/gift/reciver/`,
//             data:{
//                 reciver: reciver,
//                 giftID: giftID.id,
//                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//             },
//             success: function(response) {
//                 console.log('response from server'+response);
//               },
//             error: function(response) {
//               alert('An error occurred');
//             }
//           });
//     })
// })