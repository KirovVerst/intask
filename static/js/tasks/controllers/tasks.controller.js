/**
 * Created by Kirov on 19/11/15.
 */
(function () {
	'use strict';

	angular.module('application.tasks.controllers')
		.controller('TasksController', function (Tasks, Events, $routeParams, $window) {
			var vm = this;
			vm.event = Events.get({id: $routeParams.eventId});

			vm.new = {};

			vm.create = function () {
				Tasks.save({eventId: vm.event.id}, vm.new);
				$window.location = '/events/' + vm.event.id ;
			}

		})
})();
