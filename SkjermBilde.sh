scrot -d 1 ~/Pictures/$(date +%F-%T).png && \
	sleep 2 && \
	dunstify -h string:x-dunst-stack-tag:Scrot \
	"Bilde tatt og flyttet til ~/Pictures/"
