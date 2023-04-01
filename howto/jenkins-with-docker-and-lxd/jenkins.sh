#!/bin/bash

mkdir -p $HOME/J/jenkins_home
chmod 777 $HOME/J/jenkins_home
docker run -itd --name jenny -h jenny \
--restart=on-failure \
-p 8080:8080 -p 50000:50000 \
-v $HOME/J/jenkins_home:/var/jenkins_home jenkins/jenkins:lts-jdk11


#http://gaia:8080/cli/

curl -sL -O http://gaia:8080/jnlpJars/jenkins-cli.jar
mkdir -p ~/bin
mv jenkins-cli.jar ~/bin

# generate a token from http://gaia:8080/user/ir/configure
# keep in ~/.ssh/token-gaia as ir:token

alias jc="java -jar $HOME/bin/jenkins-cli.jar -auth @$HOME/.ssh/token-gaia -s http://gaia:8080/ -webSocket"





cat <<'EOF' >/dev/null

List installed plugins
http://master-irjenkins.dev.purestorage.com:8080/script

--
Jenkins.instance.pluginManager.plugins.each{
  plugin ->
    println ("${plugin.getDisplayName()} (${plugin.getShortName()}): ${plugin.getVersion()}")
}
--

These are extra 95
     1	PrioritySorter
     2	ace-editor
     3	ansicolor
     4	any-buildstep
     5	authentication-tokens
     6	authorize-project
     7	badge
     8	bootstrap4-api
     9	build-metrics
    10	build-name-setter
    11	build-pipeline-plugin
    12	build-user-vars-plugin
    13	buildannotator
    14	cobertura
    15	code-coverage-api
    16	command-launcher
    17	conditional-buildstep
    18	config-file-provider
    19	copyartifact
    20	custom-view-tabs
    21	cvs
    22	dashboard-view
    23	data-tables-api
    24	description-setter
    25	docker-commons
    26	docker-workflow
    27	dropdown-viewstabbar-plugin
    28	envinject
    29	envinject-api
    30	extended-read-permission
    31	external-monitor-job
    32	fail-the-build-plugin
    33	flexible-publish
    34	forensics-api
    35	global-build-stats
    36	greenballs
    37	groovy
    38	groovy-events-listener
    39	groovy-postbuild
    40	handlebars
    41	hidden-parameter
    42	htmlpublisher
    43	jacoco
    44	javadoc
    45	jdk-tool
    46	jenkins-console-logger
    47	jenkinswalldisplay
    48	jira
    49	jobConfigHistory
    50	jquery
    51	jquery-detached
    52	jsch
    53	lockable-resources
    54	mail-watcher-plugin
    55	manage-permission
    56	managed-scripts
    57	mapdb-api
    58	mask-passwords
    59	maven-plugin
    60	metrics
    61	momentjs
    62	monitoring
    63	nested-view
    64	nodelabelparameter
    65	offlineonfailure-plugin
    66	parameterized-scheduler
    67	parameterized-trigger
    68	plot
    69	popper-api
    70	popper2-api
    71	postbuild-task
    72	preSCMbuildstep
    73	prism-api
    74	prometheus
    75	purge-build-queue-plugin
    76	really-permissive-script-security
    77	rebuild
    78	run-condition
    79	saferestart
    80	saml
    81	sectioned-view
    82	shelve-project-plugin
    83	show-build-parameters
    84	sidebar-link
    85	slack
    86	swarm
    87	test-results-analyzer
    88	testInProgress
    89	testlink
    90	thinBackup
    91	throttle-concurrents
    92	translation
    93	uno-choice
    94	windows-slaves
    95	workflow-cps-global-lib



Download from http://irvm-omandal:8080/cli/
jenkins-cli.jar

Create token from http://irvm-omandal:8080/user/ir/configure

Keep in ~ir/.ssh/toke ir:token

alias jc='java -jar /home/ir/x/jenkins-cli.jar -auth @/home/ir/.ssh/token -s http://irvm-omandal:8080/ -webSocket'

jc help

jc install-plugin beer

EOF

