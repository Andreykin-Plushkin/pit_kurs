
async function learn(){    

    let response = await fetch(
        '/api/learn', 
        {
          method: 'POST',
          body: new URLSearchParams(
          	{ 
          		epochs: document.getElementById("input-epochs").value,
          		batch_size: document.getElementById("input-batch-size").value
          	}
          )
    })

  	if (response.ok) {
  		alert("Обучение завершено!")
        window.location.reload()
  	}
};


let learnButton = document.getElementById('learn-button')
learnButton.addEventListener("click", learn)


