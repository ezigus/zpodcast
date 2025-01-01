from flask import Flask, jsonify
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastplaylist import PodcastPlaylist

app = Flask(__name__)

@app.route('/api/podcasts', methods=['GET'])
def get_podcasts():
    # Placeholder for actual podcast list retrieval logic
    podcast_list = PodcastList()
    return jsonify(podcast_list.to_dict())

@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    # Placeholder for actual playlist retrieval logic
    playlist = PodcastPlaylist()
    return jsonify(playlist.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
