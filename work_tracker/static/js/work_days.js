        $(document).ready(function () {
            // Добавление нового рабочего дня
            $('#add-work-day-form').submit(function (e) {
                e.preventDefault();
                const data = {
                    date: $('#date').val(),
                    gross_income: $('#gross_income').val(),
                    extra_income: $('#extra_income').val(),
                    cash_income: $('#cash_income').val(),
                    car_wash_expenses: $('#car_wash_expenses').val()
                };

                $.post('/work_days', data, function (response) {
                    if (response.status === 'success') location.reload();
                    else alert(response.message || 'Ошибка добавления');
                });
            });

            // Редактирование рабочего дня
            $(document).on('click', '.edit-btn', function () {
                const row = $(this).closest('tr');
                const id = row.data('id');

                const date = prompt('Введите дату:', row.find('td:eq(0)').text());
                const gross_income = prompt('Грязные деньги:', row.find('td:eq(1)').text());
                const extra_income = prompt('Левак:', row.find('td:eq(3)').text());
                const cash_income = prompt('Наличные:', row.find('td:eq(4)').text());
                const car_wash_expenses = prompt('Мойка:', row.find('td:eq(5)').text());

                const data = { date, gross_income, extra_income, cash_income, car_wash_expenses };

                $.ajax({
                    url: '/work_days/' + id,
                    method: 'PUT',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function (response) {
                        if (response.status === 'success') location.reload();
                        else alert(response.message || 'Ошибка обновления');
                    },
                    error: function (xhr) {
                        console.error(xhr.responseText);
                    }
                });
            });

            // Удаление рабочего дня с подтверждением через SweetAlert2
            $(document).on('click', '.delete-btn', function () {
                const id = $(this).data('id');

                // Подтверждение удаления с помощью SweetAlert2
                Swal.fire({
                    title: 'Вы точно хотите удалить эту запись?',
                    text: "Это действие нельзя будет отменить!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#d33',
                    cancelButtonColor: '#3085d6',
                    confirmButtonText: 'Удалить',
                    cancelButtonText: 'Отмена'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Если подтверждено, отправляем запрос на удаление записи
                        $.ajax({
                            url: '/work_days/' + id,
                            method: 'DELETE',
                            success: function (response) {
                                if (response.status === 'success') {
                                    Swal.fire('Удалено!', 'Запись была успешно удалена.', 'success');
                                    location.reload();
                                } else {
                                    Swal.fire('Ошибка!', 'Что-то пошло не так при удалении записи.', 'error');
                                }
                            }
                        });
                    }
                });
            });

            // Загрузка итогов, включая мойку
            fetch('/work_days/summary')
                .then((response) => response.json())
                .then((data) => {
                    $('#total-gross-income').text(data.total_gross_income.toFixed(2));
                    $('#total-net-income').text(data.total_net_income.toFixed(2));
                    $('#total-extra-income').text(data.total_extra_income.toFixed(2));
                    $('#total-cash-income').text(data.total_cash_income.toFixed(2));
                    $('#total-car-wash-expenses').text(data.total_car_wash_expenses.toFixed(2));
                    $('#total-total').text(data.total_total.toFixed(2));
                })
                .catch((error) => console.error('Ошибка при загрузке итогов:', error));
        });

        $(document).on('click', '.lock-btn', function () {
    const $lockButton = $(this); // Кнопка замочка
    const $row = $lockButton.closest('tr'); // Строка таблицы
    const isLocked = $lockButton.data('locked'); // Текущее состояние блокировки

    // Переключение состояния блокировки
    if (isLocked) {
        $lockButton.html('🔒'); // Замок закрыт
        $row.find('.edit-btn, .delete-btn').attr('disabled', true); // Отключить редактирование и удаление
    } else {
        $lockButton.html('🔓'); // Замок открыт
        $row.find('.edit-btn, .delete-btn').attr('disabled', false); // Включить редактирование и удаление
    }

    // Обновить состояние блокировки
    $lockButton.data('locked', !isLocked);
});

document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.getElementById("app-body");

  // Сохраняемая тема
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    body.setAttribute("data-bs-theme", savedTheme);
    themeToggle.textContent =
      savedTheme === "dark" ? "Светлая тема" : "Тёмная тема";
  }

  // Логика переключателя
  themeToggle.addEventListener("click", function () {
    const currentTheme = body.getAttribute("data-bs-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";

    // Применение темы
    body.setAttribute("data-bs-theme", newTheme);

    // Сохранение в localStorage
    localStorage.setItem("theme", newTheme);

    // Текст кнопки
    themeToggle.textContent =
      newTheme === "dark" ? "Светлая тема" : "Тёмная тема";
  });
});

