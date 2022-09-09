const title = (message) => { console.log(message); };

function heading(message) {
  message.split(/[\r\n]+/).forEach((line) => { console.log('====>', line); });
}

function subheading(message) {
  message.split(/[\r\n]+/).forEach((line) => { console.log('---->', line); });
}

function info(message) {
  message.split(/[\r\n]+/).forEach((line) => { console.log('     ', line); });
}

function warning(message) {
  message.split(/[\r\n]+/).forEach((line) => { console.log('WARN ', line); });
}

function error(message) {
  message.split(/[\r\n]+/).forEach((line) => { console.error('ERROR', line); });
}

module.exports = {
  title, heading, subheading, info, warning, error,
};
