$(document).ready(function() {
	let updateForm = $('#update-task-form');
	// Обновление по нажатию
	updateForm.submit(function(e){
		// Отменяем событие чтобы не перейти на другую страницу
		e.preventDefault();
		let id = $(this).children("input[name='id']").val();
		// Массив данных с формы
		let data = $(this).serializeArray().reduce(function(obj, item) {
    		obj[item.name] = item.value;
    		return obj;
		}, {});
		// Проверка чекбокса (не вносится, если не включен)
        data['status-input'] = (data['status-input']=='on') ? 1 : 0; 

		$.ajax({
			url: '/task/'+id,
			type: 'PATCH',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify(data),
			success: function(result) {
                alert('Задача обновлена');
			}
		});
	});

	// Удаление по нажатию
	$('.delete-button').click(function() {
		// Получаем родителя
        let id = $(this).parent().parent().parent().attr("data-id");

        $.ajax({
            url: '/task/'+id,
            type: 'DELETE',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'id':id}),
            success: function(result) {
                console.log(result);
            }
        });

        $(this).parent().parent().parent().remove();
    });

	// Блок с комментариями
    let comments = $('#comments');
	if (comments) {
		let id = $('form').children("input[name='id']").val();
		$.ajax({
			type: 'get',
			url: 'https://jsonplaceholder.typicode.com/comments?postId='+id, 
			success: function(res) {
                res.forEach(function(elem){
             		//comments.after(`<div class="comment card-body bg-light mt-1"><h5 class="comment-name card-title text-info mb-0">${elem.name}</h5><h7 class="comment-email card-subtitle mb-2 text-muted">${elem.email}</h7><p class="comment-text card-text">${elem.body}</p></div>`);
										
					// <div class="comment card-body bg-light mt-1">
					var comm_card = document.createElement('div');
					comm_card.className = 'comment card-body bg-light mt-1';
					
					// <h5 class="comment-name card-title text-info mb-0">${elem.name}</h5>
					var comm_auth = document.createElement('h5');
					comm_auth.className = 'comment-name card-title text-info mb-0';
					comm_auth.innerHTML = elem.name;

					// <h7 class="comment-email card-subtitle mb-2 text-muted">${elem.email}</h7>
					var comm_email = document.createElement('h7');
					comm_email.className = 'comment-email card-subtitle mb-2 text-muted';
					comm_email.innerHTML = elem.email;
					
					// <p class="comment-text card-text">${elem.body}</p>
					var comm_text = document.createElement('p');
					comm_text.className = 'comment-text card-text';
					comm_text.innerHTML = elem.body;
					
					comments.after(comm_card);
					comm_card.append(comm_auth);
					comm_card.append(comm_email);
					comm_card.append(comm_text);
				});
			}
		});
        
	}


});