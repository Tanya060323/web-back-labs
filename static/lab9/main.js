window.onload = function() {
    loadBoxes();
};

function loadBoxes() {
    fetch('/lab9/rest-api/boxes')
        .then(function(data) {
            return data.json();
        })
        .then(function(boxes) {
            let area = document.getElementById('area');
            area.innerHTML = '';
            
            for (let i = 0; i < boxes.length; i++) {
                let box = boxes[i];
                let div = document.createElement('div');
                div.className = 'box';
                div.id = 'box-' + box.id;
                div.style.backgroundImage = 'url(' + box.img + ')';
                div.style.top = box.top + '%';
                div.style.left = box.left + '%';
                
                if (box.opened) {
                    div.classList.add('opened');
                } else {
                    if (box.need_auth) {
                        div.classList.add('locked');
                    }
                    div.onclick = function() {
                        openBox(box.id);
                    };
                }
                
                area.appendChild(div);
            }
        });
}

function openBox(id) {
    fetch('/lab9/rest-api/open/' + id, {
        method: 'POST'
    })
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(function(err) {
                throw new Error(err.error);
            });
        }
    })
    .then(function(data) {
        showModal(data.text, data.img);
        document.getElementById('count').innerText = data.unopened;
        loadBoxes();
    })
    .catch(function(error) {
        alert(error.message);
    });
}

function showModal(text, img) {
    document.getElementById('text').innerText = text;
    document.getElementById('img').src = img;
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

window.onclick = function(event) {
    let modal = document.getElementById('modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

function resetBoxes() {
    if (!confirm('Дед Мороз наполнит все коробки подарками снова. Продолжить?')) {
        return;
    }
    
    fetch('/lab9/rest-api/reset', {
        method: 'POST'
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        alert(data.message);
        location.reload();
    });
}

