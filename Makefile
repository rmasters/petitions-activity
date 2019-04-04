NS=petitions

deploy:
	kubectl apply --namespace="$(NS)" --filename=deploy/
.PHONY: deploy
