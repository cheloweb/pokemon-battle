$(document).ready(function() {
    const imageUrlBase = 'https://img.pokemondb.net/artwork/'; // Cambia esto por la URL real

    // Cargar todos los nombres de los Pokémon
    $.ajax({
        url: '/get_all_pokemons',
        method: 'GET',
        success: function(data) {
            data.forEach(function(pokemon) {
                $('#pokemon1').append(new Option(pokemon, pokemon));
                $('#pokemon2').append(new Option(pokemon, pokemon));
            });
            // Agregar cuadro de búsqueda
            $('#pokemon1').select2();
            $('#pokemon2').select2();
        }
    });

    function loadPokemonInfo(pokemon, target) {
        $.ajax({
            url: '/get_pokemon_info',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({name: pokemon}),
            success: function(data) {
                const imageUrl = imageUrlBase + data.Name.toLowerCase() + '.jpg';
                $(target).find('.pokemon-details').html(`
                    <p><strong>HP:</strong> <span class="hp-value">${data.HP}</span></p>
                    <p><strong>Generación:</strong> ${data.Generation}</p>
                    <p><strong>Tipo:</strong> ${data.Type}</p>
                    <p><strong>Altura (m):</strong> ${data.Height}</p>
                    <p><strong>Peso (kg):</strong> ${data.Weight}</p>
                `);
                $(target).find('.pokemon-image').attr('src', imageUrl).attr('alt', data.Name);
            }
        });
    }

    // Manejar selección de Pokémon
    $('#pokemon1').on('change', function() {
        loadPokemonInfo($(this).val(), '#pokemon1-info');
        $('#error-message').hide();
    });

    $('#pokemon2').on('change', function() {
        loadPokemonInfo($(this).val(), '#pokemon2-info');
        $('#error-message').hide();
    });

    // Manejar selección aleatoria de Pokémon
    $('#random1').on('click', function() {
        var options = $('#pokemon1 option');
        var randomPokemon = options[Math.floor(Math.random() * options.length)].value;
        $('#pokemon1').val(randomPokemon).trigger('change');
    });

    $('#random2').on('click', function() {
        var options = $('#pokemon2 option');
        var randomPokemon = options[Math.floor(Math.random() * options.length)].value;
        $('#pokemon2').val(randomPokemon).trigger('change');
    });

    // Manejar el botón de predicción
    $('#predict-btn').on('click', function() {
        const pokemon1 = $('#pokemon1').val();
        const pokemon2 = $('#pokemon2').val();

        // Manejo de errores si no hay selección
        if (!pokemon1 || !pokemon2) {
            $('#error-message').text('Debe seleccionar 2 pokémon para la batalla antes de iniciar').show();
            return;
        }

        // Mostrar modal con mensaje de carga
        $('#loadingMessage').show();
        $('#winnerDisplay').hide();
        $('#winnerModal').modal('show');

        // Simulación de la batalla con retraso
        setTimeout(function() {
            $.ajax({
                url: '/predict_winner',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({pokemon1: pokemon1, pokemon2: pokemon2}),
                success: function(data) {
                    const winnerImageUrl = imageUrlBase + data.winner.toLowerCase() + '.jpg';
                    $('#winnerName').text(data.winner);
                    $('#winnerImage').attr('src', winnerImageUrl);
                    $('#loadingMessage').hide();
                    $('#winnerDisplay').show();

                    // Agregar la batalla al historial
                    $('#battle-history-table tbody').append(`
                    <tr>
                        <td>${pokemon1}</td>
                        <td>${pokemon2}</td>
                        <td>${data.winner}</td>
                    </tr>
                    `);
                }
            });
        }, 1000); // Retraso de 1 segundo para simular la batalla
    });
});
