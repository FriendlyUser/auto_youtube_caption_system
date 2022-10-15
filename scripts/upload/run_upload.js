// import uploadVideo from upload_to_youtube

const uploadVideo = require('./upload_to_youtube').uploadVideo

const title = 'Kage no Jitsuryokusha ni Naritakute Opening HIGHEST by OxT using ai'
const description = 'Opening translation for Kage no Jitsuryokusha ni Naritakute using ai, issues from dalle'
const tags = ['kage no jitsuryokusha ni Naritakute', 'opening']

uploadVideo(title, description, tags)