const ghpages = require('gh-pages');

ghpages.publish('frontend/public', {
    branch: 'gh-pages',
    repo: 'https://github.com/EshwarDheekonda/OneMoat.git',
    user: {
        name: 'EshwarDheekonda',
        email: 'eshwardheekonda@gmail.com'
    }
}, function(err) {
    if (err) {
        console.error('Error publishing to GitHub Pages:', err);
    } else {
        console.log('Successfully published to GitHub Pages!');
    }
});
