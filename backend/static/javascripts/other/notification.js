const ntfContainer= document.getElementById("nft-holder");

const iconsDict={
    'Transaction':'paid',
    'Referral': 'group',
    'Notice': 'info',
    'Achievement': 'trophy',
    'Site Blog': 'description',
}


fetch('/accounts/user/notifications/')
.then(response => response.json())
.then(response => {
    ntfContainer.innerHTML= ''
    for(x in response.nfts){
        // console.log(response.nfts[x])
        const nftID= response.nfts[x].uuid
        const nftT= response.nfts[x].notification_type
        const msg= response.nfts[x].notification
        const status= response.nfts[x].read
        const actionRequired= response.nfts[x].action_required
        const actionTodo= response.nfts[x].actionTodo
        const action= response.nfts[x].action
        ntfContainer.innerHTML = `<div class="note" id="nft-cont">
    <div id="note-head">
    <h1><i class="material-symbols-rounded">${iconsDict[nftT]}</i> ${nftT}</h1>
    <h1 id="status">${status == 'True'?'Read':'Unread'}</h1>
    </div>
    <div class="notemessage">
    <span>${msg}</span>
    <div id="actions-container">
    ${status == 'False'?`<button class='btn-mark' id="nft-mark" name="${nftID}">Mark as read</button>`:''}
    ${actionRequired == 'True'?`<button class='btn-mark' id="actionBtn" name="${actionTodo}">${action == 'Done'?'Action Completed':'Action required'}</button>`:''}
    <button class='btn-mark' id="deleteBtn" name="${nftID}">Delete</button>
    </div>
    </div>
    </div>` + ntfContainer.innerHTML
    }
    const nfts= document.querySelectorAll('#nft-cont');
    
    nfts.forEach((x)=>{
       const statusEl= x.querySelector('#status');
       try {
           let readBtns= x.querySelector('#nft-mark')   
           readBtns.addEventListener('click', function(e){
            const id= e.target.name
            $.ajax({
                type: "POST",
                url: "/accounts/notifications-update/",
                data: {
                    nftID: `${id}`,
                },
                success: function(data){
                   if(data.status == "ok"){
                    statusEl.textContent= 'Read'
                    readBtns.remove()
                   }
                },
                error: function (xhr, status, error) {
                  console.error("Error:", error);
                  alert(error);
                },
              });
           })
       } catch (error) {} 
       try {
           let actionRequiredBtn= x.querySelector('#actionBtn')
           actionRequiredBtn.addEventListener('click', function(e){
            window.location.href= e.target.name
           })
       } catch (error) {}
       const deleteBtn= x.querySelector('#deleteBtn');
       deleteBtn.addEventListener('click',function(e){
        const nftID= e.target.name
        $.ajax({
            type: "POST",
            url: "/accounts/notifications-delete/",
            data: {
                nftID: `${nftID}`,
            },
            success: function(data){
               if(data.status == "ok"){
                x.remove()
               }
            },
            error: function (xhr, status, error) {
              console.error("Error:", error);
              alert(error);
            },
          });
       })
    })
})