const postData = async (url = '', data = {}) => {
  // Формируем запрос
  const response = await fetch(url, {
    // Метод, если не указывать, будет использоваться GET
    method: 'POST',
   // Заголовок запроса
    headers: {
      'Content-Type': 'application/json'
    },
    // Данные
    body: JSON.stringify(data)
  });
  return response.json();
}

function dell(id, name){
    postData('/web/dell/'+name+'/'+id)
      .then((data) => {
        console.log(data);
      });
}

document.querySelectorAll(".btn-dell").forEach(el => {
    el.addEventListener("click", (e)=>{
        dell(e.currentTarget.getAttribute("data-id"),e.currentTarget.getAttribute("data-name"));
        e.currentTarget.parentElement.parentElement.classList.add("visually-hidden");
    })
})