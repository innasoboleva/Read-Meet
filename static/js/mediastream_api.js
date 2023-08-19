// Handling video stream
const localVideo = document.getElementById('video-container');

// Need to be able to have permissions for audio and video
const mediaStreamConstraints = {
    audio: true,
    video: true
 };

 navigator.mediaDevices.getUserMedia( mediaStreamConstraints )
.then( resultingMediaStream => {
    // connecting video block with camera stream
   let video = document.querySelector('#video-block');
   if ('srcObject' in video) {
    video.srcObject = resultingMediaStream;
   }

   const record = document.getElementById('start-recording');
   const stopRecording = document.getElementById('stop-recording');
   const yourVideo = document.getElementById('your-video');

   const mediaRecorder = new MediaRecorder(resultingMediaStream);
   // video data goes into this array
   let chunks = [];

   // listeners for creating video
   record.addEventListener('click', (ev) => {
    mediaRecorder.start()
    ev.target.disabled = true;
    stopRecording.disabled = false;
    console.log(mediaRecorder.state);
   });

   stopRecording.addEventListener('click', (ev) => {
    mediaRecorder.stop()
    ev.target.disabled = true;
    record.disabled = false;
    console.log(mediaRecorder.state);
   });
   // called when chunk is available
   mediaRecorder.ondataavailable = (ev) => {
    chunks.push(ev.data);
   };
   mediaRecorder.onstop = () => {
    // creating video from chunks
    const blob = new Blob(chunks, { type: "video/mp4" });
    // cleaning array
    chunks =[];
    let videoURL = URL.createObjectURL(blob);
    // showing video made by user
    yourVideo.src = videoURL;
   };

})
.catch(NotAllowedError => {
    // Permissions were denied
    console.error('Permissions for audio and video were denied.');
})
.catch(error => {
    console.error('Error accessing audio and video:', error);
});
