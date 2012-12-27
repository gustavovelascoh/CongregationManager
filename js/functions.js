function sendData(url, data)
{
	$.ajax({
		type: 'POST',
		url: url,
		data: data,
		success: function(data){
			if (data == 'success'){
				alert("Informacion guardada!!");
			}
			else if (data == 'error'){
				alert("Error al guardar la informacion");
			}else{
				return data;
			}
		}
	});
}
