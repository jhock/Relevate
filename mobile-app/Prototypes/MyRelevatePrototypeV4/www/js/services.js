angular.module('starter.services', [])


/*
 - 1 Month mandatory token unless manual logout, so make
   sure to log in with that if it is saved and not request another login.
 - Make sure to use saved, secret, database password,etc.. in group admin document.
GET REQUESTS FOR THINGS:
  $http({
  method: 'GET',
  url: 'DevDatabaseHost/{WhatIWant}'
  }).then(function successCallback(response){

  }, function errorCallback(response) {

  });
*/

//Factory for quiz data access
.factory('Quizzes', function(){

  //Local quiz objects for testing
  var quizzes = [
  {
    id: 1,
    title: 'Quiz #1',
    description: 'A quick quiz to see how well you can romance!',
    length: '10m',
    type: 'Q',
    questions: [{
      id:1,
      text: "Enter in A",
      options: [{
        letter: 'A',
        option: 'Yes'
      },
      {
        letter: 'B',
        option: 'No'
      }]
    }]
  },
  {
    id: 2,
    title: 'Quiz #2',
    description: 'Quiz about your past romantic interests',
    length: '30m',
    type: 'S',
    questions: [{
      id:1,
      text: "Enter in A",
      options: [{
        letter: 'A',
        option: 'Yes'
      },
      {
        letter: 'B',
        option: 'No'
      }]
    }]
  },
  {
    id: 3,
    title: 'Quiz #3',
    description: 'Quiz about your last couple dates',
    length: '15m',
    type: 'S',
    questions: [{
      id: 1,
      text: "Enter in A",
      options: [{
        letter: 'A',
        option: 'Yes'
      },
      {
        letter: 'B',
        option: 'No'
      }]
    }]
  }];

  //Basic return functions
	return {
		all: function() {
			return quizzes;
		},
		remove: function(quiz){
			quizzes.splice(quizzes.indexOf(quiz),1);
		},
		get: function(quizId){
			for (var i = 0; i < quizzes.length; i++){
				if (quizzes[i].id === parseInt(quizId)){
					return quizzes[i];
				}
			}
			return null;
		}


		};
	})

//Factory for journal data access
.factory('Journals', function(){
  var journals = [];

    return {
    all: function() {
      return journals;
    },
    add: function(journalEntry,newtitle){
      var newJournal = {
        id: journals.length+1,
        title: String(newtitle),
        text: String(journalEntry),
        date: new Date()
       };
      journals.splice(journals.length,0,newJournal);
    },
    remove: function(journalId){
      journals.splice(journals.indexOf(journalId),1);
    },
    get: function(journalId){
      for (var i = 0; i < journals.length; i++){
        if (journals[i].id === parseInt(journalId)){
          return journals[i];
        }
      }
      return null;
    }


    };
  })

//Factory for new data access
.factory('News', function(){

  //Local news articles for testin
  var news = [
  {
    id : 1,
    author: 1,
    title: '5 Relationship Tips',
    descshort: 'Check Out these 5 tips on relationships!',
    desclong: 'These 5 tips will help you and your partner on the best way to carry on a long term relationship.',
    image: 'img/RelevateLogoL.png',
    iconImage:'img/RelevateLogoL.png',
    type: 'PDF',
    content: 'img/valentinesResolutions.pdf',
    date: new Date(),
    tags:[1,3,4,5]
  },
  {
    id : 2,
    author: 1,
    title: '5 Relationship Tips',
    descshort: 'Check Out these 5 tips on relationships!',
    desclong: 'These 5 tips will help you and your partner on the best way to carry on a long term relationship.',
    image: 'img/RelevateLogoL.png',
    iconImage: 'img/RelevateLogoL.png',
    type: 'PDF',
    content: 'img/valentinesResolutions.pdf',
    date: new Date(),
    tags:[0,1,2]
  },
  {
    id : 3,
    author: 2,
    title: '5 Relationship Tips',
    descshort: 'Check Out these 5 tips on relationships!',
    desclong: 'These 5 tips will help you and your partner on the best way to carry on a long term relationship.',
    image: 'img/RelevateLogoL.png',
    iconImage: 'img/RelevateLogoL.png',
    type: 'PDF',
    content: 'img/valentinesResolutions.pdf',
    date: new Date(),
    tags:[1,2,3,4,5]
  },
  {
    id : 4,
    author: 2,
    title: '5 Relationship Tips',
    descshort: 'Check Out these 5 tips on relationships!',
    desclong: 'These 5 tips will help you and your partner on the best way to carry on a long term relationship.',
    image: 'img/RelevateLogoL.png',
    iconImage: 'img/RelevateLogoL.png',
    type: 'Web',
    content: 'http://www.google.com/',
    date: new Date(),
    tags:[1,2,3,4,5]
  }
  ];

    return {
    all: function() {
      return news;
    },
    remove: function(newsArticle){
      news.splice(news.indexOf(newsArticle),1);
    },
    get: function(newsArticleId){
      for (var i = 0; i < news.length; i++){
        if (news[i].id === parseInt(newsArticleId)){
          return news[i];
        }
      }
      return null;
    },
    getByAuthor: function(authorId){
      var list = [];
      for (var i = 0;i < news.length; i++){
         if(news[i].author === parseInt(authorId)){
          list.push(news[i]);
         }
      }
      return list;
    },
    getByList: function(idList){
      var list = [];
      console.log(idList);
      for (var i = 0; i < idList.length; i++){
          list.push(news[idList[i]-1]);
         }
      return list;
      },
    getByTags: function(tags){
      var list = [];
      for(var i = 0; i < news.length; i++){
        for(var k = 0; k < news[i].tags.length; k++)
        {
          for(var tag in tags)
          {
            if(tag == news[i].tags[k])
            {
              list.push(news[i]);
              break;
            }
          }
        }
      }
      return list;
    }
    };
})

//Factory for contributors
.factory('Contributors', function(){

  /*
  To be implemented once API is done
  - In the all and get functions, just return from API calls what is needed,
    possibly just cache the first X amount of contributors needed, and append to the local list
    as needed from the web calls.
  */
  //Local news articles for testin
  var contributors = [
  {
    id : 1,
    name: 'Dr. Amber Vennum',
    education: ['MA- University of Houston-Clear Lake in Marriage and Family Therapy in 2007', 'PhD- The Florida State University  in Marriage and Family Therapy in 2011'],
    employmentInfo: 'Assistant Professor of Marriage and Family Therapy at Kansas State University',
    description: 'I am passionate about finding ways to give adolescents and young adults the best chance possible of having stable, healthy relationships throughout their lives. I am currently researching risk and resiliency factors that impact romantic relationship stability and health for adolescents and young adults and the long-term impact of those factors. I am also interested in increasing access to mental health services and relationship research by working with high schools and developing online and mobile resources.',
    expertiseAreas: [7,8,9,10],
    websiteLinks: ['http://www.he.k-state.edu/fshs/people/avennum/'],
    profilePic: 'img/AmberVennum.jpg'
  },
  {
    id : 2,
    name: 'Dr J.Kale Monk',
    education: ['M.S. – Kansas State University, Marriage and Family Therapy, 2013', 'B.S. – Kansas State University, Psychology and Family Studies, 2010'],
    employmentInfo: 'Ph.D. Student, Instructor, and Graduate Research Assistant, The University of Illinois at Urbana-Champaign, Human Development and Family Studies',
    description: 'I am currently seeking advanced training in intimate relationship research in order to provide insight into how young adults and adults can create healthy, stable unions. My main interest is helping couples establish and maintain quality in their relationships, especially during stressful transitions (e.g., the transition to adulthood, the transition to marriage).',
    expertiseAreas: [7,8,11],
    websiteLinks: ['http://hdfs.illinois.edu/directory/graduate/jkmonk'],
    profilePic: 'img/person.png'
  }
  ];

    return {
    all: function() {
      return contributors;
    },
    get: function(contributorId){
      for (var i = 0; i < contributors.length; i++){
        if (contributors[i].id === parseInt(contributorId)){
          return contributors[i];
        }
      }
      return null;
    },
    getByTags: function(tags){
      var list = [];
      for(var i = 0; i < contributors.length; i++){
        for(var k = 0; k < contributors[i].expertiseAreas.length; k++)
        {
          for(var tag in tags)
          {
            if(tag == contributors[i].expertiseAreas[k])
            {
              list.push(contributors[i]);
              break;
            }
          }
        }
      }
      return list;
    }
  }

  })

.factory('Favorites', function(){
  var favorites = [];
  return {
    all: function(){
      return favorites;
    },
    add: function(articleId){
      var favId = articleId;
      var index = favorites.indexOf(favId);
      favorites.push(articleId);
      return true;
    },
    get: function(articleId){
      var favId = articleId;
      var index = favorites.indexOf(favId);
      if (index == -1){
        return false;
      }
      else{
        return favorites[index];
      }
    },
    find: function(articleId){
      var favId = articleId;
      var index = favorites.indexOf(favId);
      if (index == -1){
        return false;
      }
      else{
        return true;
      }
    },
    remove: function(articleId){
      var favId = articleId;
      var index = favorites.indexOf(favId);
      if(index == -1){
        return false;
      }
      else{
        favorites.splice(index,1);
        return true;
      }
    }
  }
})

.factory('Users', function(){

  /*
  To be implemented once API is done
  - Same as with the contributors, need to make calls through API to get official user information.
  - Need to authenticate here as well, and make sure that across all other pages that the user's session token is available, otherwise force to login/register screen.
  - Will only need one user at a time, except in the case when certain other user information is needed, such as on comments and other public posts.
  */
  var users = [
    {id:1,
     email:'ajbeahm@ksu.edu',
     password:'Password1'}
     ];

    return {
    get: function(email, password){
      for (var i = 0; i < users.length; i++){
        if (users[i].email == email){
          if(users[i].password == password){
          return users[i];
           }
        }
      }
      return null;
    },
    getEmail: function(email){
      for (var i = 0; i < users.length; i++){
        if (users[i].email == email){
          return true;
           }
         }
        return false;
      },
    add: function(newemail, newpassword){
      var newUser = {
        id: users.length+1,
        email: String(newemail) ,
        password: String(newpassword)
      };
      users.splice(users.length,0,newUser);
    }

  }

})


.factory('Tags', function(){
  /*
  To be implemented
  -Will either needs Josh to make sure that the tags/experience is a part of the contributor profile (i.e. relevant experience)
  -Otherwise, needs to parse out these from the contributor profile in order to correctly show these tags.
  */
  var tags = [
  {
    id:0,
    name:'Relationship'
  },
  {
    id:1,
    name:'Romance'
  },
  {
    id:2,
    name:'Trust'
  },
  {
    id:3,
    name: 'Children'
  },
  {
    id:4,
    name: 'Cheating'
  },
  {
    id:5,
    name: 'Lying'
  },
  {
    id:6,
    name: 'Growth'
  },
  {
    id:7,
    name: 'Mental health'
  },
  {
    id:8,
    name: 'Romantic relationship stability'
  },
  {
    id:9,
    name: 'Relationship education'
  },
  {
    id:10,
    name: 'Healthy romantic relationships'
  },
  {
    id:11,
    name: 'Military couples'
  }
  ];

  return {
    all: function(){
      return tags;
    },

    get: function(tagList){
      var matchTags = new Array(tagList.length);
      var count = 0;
      for(var k = 0; k < tagList.length; k++)
      {
        matchTags[k] = tags[tagList[k]];
      }
      return matchTags;
    },

    getIds: function(tagList){
      var list = [tagList.length];
      for(var k = 0; k < tagsList.length; k++)
      {
        for(var i = 0; i < tags.length; i++)
        {
          if(tags[i].name == tagList[k])
          {
            list.push(tags[i].id);
            break;
          }
        }
      }
      return list;
    }

  }

});