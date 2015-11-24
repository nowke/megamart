module.exports = function(grunt) {

	// require('load-grunt-tasks')(grunt);

	grunt.initConfig({
		sass: {
			options: {
				includePaths: ['megamart/static/build/scss']
			},
			dist: {
				options: {
					outputStyle: 'compressed'
				},
				files: {
					'megamart/static/dist/css/styles.min.css': 'megamart/static/build/scss/styles.scss',
					'megamart/static/dist/css/fonts.min.css': 'megamart/static/build/scss/fonts.scss',
					'megamart/static/dist/css/simpleGrid.min.css': 'megamart/static/build/scss/simpleGrid.scss',
					'megamart/static/dist/css/dashboard.min.css': 'megamart/static/build/scss/dashboard.scss',
					'megamart/static/dist/css/print.min.css': 'megamart/static/build/scss/print.scss',
				}
			}
		},

		copy: {
			main: {
				files: [
					{
						expand: true, 
						cwd: 'megamart/static/build/css/', 
						src: ['**'],
						dest: 'megamart/static/dist/css',
					},
					{
						expand: true, 
						cwd: 'megamart/static/build/img/', 
						src: ['**'],
						dest: 'megamart/static/dist/img',
					},
					{
						expand: true, 
						cwd: 'megamart/static/build/js/', 
						src: ['**'],
						dest: 'megamart/static/dist/js',
					},
					{
						expand: true, 
						cwd: 'megamart/static/build/fonts/', 
						src: ['**'],
						dest: 'megamart/static/dist/fonts',
					},
				],
			},
		},

		watch: {
			grunt: { files: ['Gruntfile.js'] },

			sass: {
				files: 'megamart/static/build/scss/**/*.scss',
				tasks: ['sass']
			},
		}
	});

	grunt.loadNpmTasks('grunt-sass');
  	grunt.loadNpmTasks('grunt-contrib-watch');
  	grunt.loadNpmTasks('grunt-contrib-copy');

  	grunt.registerTask('build', ['sass', 'copy']);
	grunt.registerTask('default', ['build', 'watch']);
};