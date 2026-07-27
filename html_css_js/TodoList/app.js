const todoForm = document.querySelector("#todoForm");
const todoInput = document.querySelector("#todoInput");
const todoList = document.querySelector("#todoList");

const emptyMessage = document.querySelector("#emptyMessage");

const totalCount = document.querySelector("#totalCount");
const doneCount = document.querySelector("#doneCount");
const leftCount = document.querySelector("#leftCount");

updateSummary();

todoForm.addEventListener("submit", function(e){

    e.preventDefault();

    const text = todoInput.value.trim();

    if(text===""){
        alert("할 일을 입력하세요.");
        todoInput.focus();
        return;
    }

    addTodo(text);

    todoInput.value="";
    todoInput.focus();
});

function addTodo(text){

    const li=document.createElement("li");
    li.className="todo-item";

    const left=document.createElement("div");
    left.className="left";

    const checkbox=document.createElement("input");
    checkbox.type="checkbox";

    const span=document.createElement("span");
    span.textContent=text;

    left.appendChild(checkbox);
    left.appendChild(span);

    const actions=document.createElement("div");
    actions.className="todo-actions";

    const doneBtn=document.createElement("button");
    doneBtn.textContent="완료";
    doneBtn.className="done-button";

    const deleteBtn=document.createElement("button");
    deleteBtn.textContent="삭제";
    deleteBtn.className="delete-button";

    actions.appendChild(doneBtn);
    actions.appendChild(deleteBtn);

    li.appendChild(left);
    li.appendChild(actions);

    todoList.appendChild(li);

    checkbox.addEventListener("change",function(){

        li.classList.toggle("done");

        updateSummary();

    });

    doneBtn.addEventListener("click",function(){

        checkbox.checked=!checkbox.checked;

        li.classList.toggle("done");

        updateSummary();

    });

    deleteBtn.addEventListener("click",function(){

        li.remove();

        updateSummary();

    });

    updateSummary();

}

function updateSummary(){

    const items=document.querySelectorAll(".todo-item");

    const done=document.querySelectorAll(".todo-item.done");

    totalCount.textContent=items.length;
    doneCount.textContent=done.length;
    leftCount.textContent=items.length-done.length;

    if(items.length===0){
        emptyMessage.style.display="block";
    }else{
        emptyMessage.style.display="none";
    }

}