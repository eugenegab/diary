import { dateToInput } from '/static/js/formatDate.js';

document.addEventListener("DOMContentLoaded", function () {
    const dateField = document.getElementById('date-field')
    const rightArrow = document.getElementById('right-arrow');
    rightArrow.addEventListener('click', function () {
        const inputDate = new Date(dateField.value);
        inputDate.setDate(inputDate.getDate() + 1);
        dateField.value = dateToInput(inputDate, 10);
        window.location.href = '/' + dateField.value
    });

    const leftArrow = document.getElementById('left-arrow');
    leftArrow.addEventListener('click', function () {
        const inputDate = new Date(dateField.value);
        inputDate.setDate(inputDate.getDate() - 1);
        dateField.value = dateToInput(inputDate, 10);
        window.location.href = '/' + dateField.value
    });

    dateField.addEventListener('change', async function () {
        window.location.href = '/' + dateField.value
    });
});