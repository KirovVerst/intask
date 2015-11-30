(function () {
	'use strict';


	angular
		.module('application.static.controllers')
		.controller('SidebarController', function (Events, $http, $scope, Auth, $window, $routeParams) {

			var vm = this;
			vm.isLoggedIn = !!Auth.getToken();
			if (vm.isLoggedIn) {
				vm.events = Events.query();
			}


		});
})();
