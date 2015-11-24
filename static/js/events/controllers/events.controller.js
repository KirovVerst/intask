(function () {
	'use strict';


	angular
		.module('application.events.controllers')
		.controller('EventsController', function (Events, $http, $scope, Auth, $window, $routeParams) {

			var vm = this;
			vm.isLoggedIn = !!Auth.getToken();
			vm.title = "Events";
			vm.new = {};

			vm.events = Events.query();
			vm.create = function () {
				var newEvent = Events.save({
					title: vm.new.title,
					description: vm.new.description,
					event_header: Auth.getUserId()
				});
				$window.location = "/";
			};
			vm.delete = function (id) {
				Events.delete({id: id});
				vm.events = Events.query();
				$window.location = "/";
			};

			if ($routeParams.eventId) {
				vm.currentEvent = Events.get({id: $routeParams.eventId});
			}


		});
})();
