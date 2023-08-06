(function() {
    var app = new Vue({
        el: '#app',
        data() {
            return {
                config: {},
                defaultTemperatures: [4.5, 30],
                responseMessage: null,
                responseBody: null,
                thermostatStatus: null
            }
        },
        async mounted() {
            this.config = (await axios.get('/api/config')).data;
            // https://stackoverflow.com/a/55379279
            this.config.thermostats.forEach(t => this.$set(t, 'temperature', 30));
        },
        methods: {
            getThermostatStati: function() {
                this
                    .request('/api/thermostats/status', null, 'get')
                    .then(response => {
                        this.thermostatStatus = response.data;
                    });
            },
            wakeupHost: function(name) {
                this.request('/api/wake-on-lan', { name }, 'post');
            },
            changeToAutomatic: (name) => {
                this.request('/api/thermostats/change-to-automatic', { name }, 'post');
            },
            enableBoost: (name) => {
                this.request('/api/thermostats/set-boost', { name }, 'post');
            },
            changeTemperatureTo: function(name, temperature) {
                this.request('/api/thermostats/change-temperature', { name, temperature }, 'post');
            },
            request: function(url, data, method) {
                console.log('Requesting', arguments);
                return axios({
                        url,
                        method,
                        data
                    })
                    .then((response) => {
                        this.setDebugInfo(`code ${response.status}`, response);
                        return response;
                    })
                    .catch((error) => {
                        this.setDebugInfo(error.message, error.response);
                    });
            },
            setDebugInfo: function(title, body) {
                this.responseMessage = title;
                this.responseBody = JSON.stringify(body, null, "\t");
            }
        }
    });
})();