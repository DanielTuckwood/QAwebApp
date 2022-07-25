const noteID = views.new_note.noteID

function deleteNote(noteID) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteID })
    }).then((_res) => {
        window.location.href = "/note";
    });
}