(function () {
    /* globals jasmineRequire */
    'use strict';

    var OldExceptionFormatter = jasmineRequire.ExceptionFormatter(),
        oldExceptionFormatter = new OldExceptionFormatter();

    jasmineRequire.ExceptionFormatter = function () {
        function ExceptionFormatter() {
            this.message = oldExceptionFormatter.message;
            this.stack = function (error) {
                var errorMsg = null;

                if (error) {
                    errorMsg = error.stack.split('\n').slice(0, 10).join('\n');
                }

                return errorMsg;
            };
        }

        return ExceptionFormatter;
    };
}());
