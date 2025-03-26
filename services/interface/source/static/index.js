function converterParaUTC(dataStr) {
    let data = new Date(dataStr);
    let ano = data.getFullYear();
    let mes = String(data.getMonth() + 1).padStart(2, '0');
    let dia = String(data.getDate()).padStart(2, '0');
    let hora = String(data.getHours()).padStart(2, '0');
    let minuto = String(data.getMinutes()).padStart(2, '0');
    let segundo = String(data.getSeconds()).padStart(2, '0');
    return `${ano}-${mes}-${dia}${hora}${minuto}${segundo}`;
}

function validateDates() {
    const initialDate = document.getElementById('initial-date').value;
    const finalDate = document.getElementById('final-date').value;
    const currentDate = new Date();

    // Converts the current date to the format that is used in datetime-local inputs
    const currentDateFormatted = currentDate.toISOString().slice(0, 16);

    // Checks if the end date is not before the start date or after the current date
    if (finalDate < initialDate) {
        alert('A data final não pode ser menor que a data inicial.');
        return false;
    } else if (finalDate > currentDateFormatted) {
        alert('A data final não pode ser maior que a data atual.');
        return false;
    }
    
    const params = new URLSearchParams({
        initial_date: converterParaUTC(initialDate),
        final_date: converterParaUTC(finalDate),
    }).toString();

    window.location.href = `/?${params}`;
    return false;
}

