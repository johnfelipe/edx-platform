/**
 *  Store data to enroll learners into the course
 */
;(function (define) {
    'use strict';

    define([
            'backbone'
        ],
        function( Backbone) {
            return Backbone.Model.extend({
                defaults: {
                    course_id: '',
                    optIn: false,
                },
                urlRoot: '/api/commerce/v0/baskets/'
            });
        }
    );
}).call(this, define || RequireJS.define);
