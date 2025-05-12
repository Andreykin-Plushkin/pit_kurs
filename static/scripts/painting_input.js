let canvas,ctx;
let mouseX,mouseY,mouseDown=0;
let touchX,touchY;


function init() {
    canvas = document.getElementById('user-input');
    ctx = canvas.getContext('2d');

    if(ctx) {

        clearCanvas()

        canvas.addEventListener('mousedown', sketchpad_mouseDown, false);          
        canvas.addEventListener('mousemove', sketchpad_mouseMove, false);          
        window.addEventListener('mouseup', sketchpad_mouseUp, false);           
    }
}

function draw(ctx,x,y,isDown) {
    if(isDown) {  
        ctx.beginPath();
        ctx.strokeStyle = "white";     
        ctx.lineWidth = '5';     
        ctx.lineJoin = ctx.lineCap = 'square';   
        ctx.moveTo(lastX, lastY);      
        ctx.lineTo(x,y);    
        ctx.closePath();   
        ctx.stroke(); 
    }   

  lastX = x; 
  lastY = y; 
}


function sketchpad_mouseDown() {
    mouseDown=1;    
    draw(ctx, mouseX, mouseY, false);
}

function sketchpad_mouseUp() {   
    mouseDown=0;
}

function sketchpad_mouseMove(e) {
    getMousePos(e);
    if (mouseDown==1) {
        draw(ctx, mouseX, mouseY, true);
    }
}

function getMousePos(e) {    
    if (!e)        
        var e = event;     
    if (e.offsetX) {       
        mouseX = e.offsetX;        
        mouseY = e.offsetY;    
    }    
}

let clearButton = document.getElementById('clear__button')

clearButton.addEventListener("click", clearCanvas)

function clearCanvas() { 
    preprocessCanvas() 
    ctx.clearRect(0, 0, canvas.width, canvas.height); 
    ctx.fillStyle = "black"
    ctx.fillRect(0, 0, canvas.width, canvas.height)
}


function preprocessCanvas(){
    let image = canvas.toDataURL('image/png').split(',')[1]
    return image
}



let predictButton = document.getElementById('predict__button')
predictButton.addEventListener("click", predict)


async function predict(){     
    let response = await fetch(
        '/api/predict', 
        {
          method: 'POST',
          body: new URLSearchParams({ image: preprocessCanvas() })
    })
        .then((response) => response.json())
        .then((data) => {
            alert("Ответ : " + data.answer)
        })

};

init()