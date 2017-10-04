// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic','starter.controllers', 'starter.services', 'ngCordova'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins.Keyboard && window.cordova.plugins) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });
})

.config(function($stateProvider, $urlRouterProvider) {

  $stateProvider
    //Note: the auth and register states are not part of the app state, as side-menu access is not granted yet.
    //These are more like splash screens before the actual app.

    //Routing for the login page
    .state('auth', {
      url: '/auth',
      templateUrl: 'templates/authsplash.html',
      controller: 'AuthCtrl'
    })

    //Routing for the register page
    .state('register', {
      url: '/register',
      templateUrl: 'templates/register.html',
      controller: 'RegCtrl'
    })

    //General routing for the app menu. Sets an abstract state for the menu items to append to.
    .state('app', {
    url: '/app',
    abstract: true,
    templateUrl: 'templates/menu.html',
    controller: 'AppCtrl'
  })

   //Routing for the about page.
   .state('app.about', {
    url: '/about',
    views: {
      'menuContent' : {
        templateUrl: 'templates/about.html',
        controller: 'AboutCtrl'
      }
    }
   })

   //Routing for the newsfeed page.
   .state('app.newsfeed',{
    url: '/newsfeed',
    views: {
      'menuContent': {
        templateUrl: 'templates/newsfeed.html',
        controller: 'NewsFeedCtrl'
      }
    }
   })

   //Routing for the individual newfeed article page. NOT ACTIVE
   .state('app.newsarticle', {
    url: '/newsfeed/:newsArticleId',
    views: {
      'menuContent' : {
        templateUrl: 'templates/newsArticle.html',
        controller: 'NewsArticleCtrl'
      }
    }
   })

   //Routing for the community page.
   .state('app.community',{
    url: '/community',
    views: {
      'menuContent': {
        templateUrl: 'templates/community.html',
        controller: 'CommunityCtrl'
      }
    }
   })

   //Routing for the search page.
  .state('app.search', {
    url: '/search',
    views: {
      'menuContent': {
        templateUrl: 'templates/search.html',
        controller: 'SearchCtrl'
      }
    }
  })

  //Routing for the MyData page, will be a base for others to come.
  .state('app.mydata', {
    url: '/mydata',
    cache: false,
    views: {
      'menuContent': {
        templateUrl: 'templates/mydataV2.html',
        controller: 'MyDataCtrl'
        }
      }
  })

  //Routing for the initial MyData page.
  .state('app.mydataInit', {
    url: '/mydata/mydataInit',
    cache: false,
    views:{
      'menuContent': {
        templateUrl: 'templates/mydataInit.html',
        controller: 'MyDataCtrl'
      }
    }
  })

  //Routing for the journaling page
  .state('app.journal', {
    url: '/journal',
    views:{
      'menuContent': {
        templateUrl: 'templates/journal.html',
        controller: 'JournalCtrl'
      }
    }
  })

  //Routing for the quizzes all page
  .state('app.quizzes', {
    url: '/quizzes',
    views: {
      'menuContent': {
        templateUrl: 'templates/quizzes.html',
        controller: 'QuizzesCtrl'
      }
    }
  })

  //Routing for the individual quiz page.
  .state('app.quiz', {
    url: '/quizzes/:quizId',
    views: {
      'menuContent': {
        templateUrl: 'templates/quiz.html',
        controller: 'QuizCtrl'
      }
    }
  })

  //Routing for the favorites page
  .state('app.favorites' , {
    cache: false,
    url: '/favorites',
    views: {
      'menuContent': {
        templateUrl: 'templates/favorites.html',
        controller: 'FavoritesCtrl'
      }
    }
  })

  //Routing for the contributors all page
  .state('app.contributors', {
    url: '/contributors',
    views: {
      'menuContent': {
        templateUrl: 'templates/contributors.html',
        controller: 'ContributorsCtrl'
      }
    }
  })

  //Routing for the individual contributor page.
  .state('app.contributor', {
    url: '/contributors/:contributorId',
    views: {
      'menuContent': {
        templateUrl: 'templates/contributor.html',
        controller: 'ContributorCtrl'
      }
    }
  });
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/auth');
});
