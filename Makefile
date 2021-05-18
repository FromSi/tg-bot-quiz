docker = docker-compose -f ./docker-compose.yml

.PHONY: run
run:
	-${docker} stop
	${docker} build
	${docker} up -d

.PHONY: stop
stop:
	${docker} stop

.PHONY: create_quiz
create_quiz:
	${docker} exec python sh -c "python create_quiz.py"