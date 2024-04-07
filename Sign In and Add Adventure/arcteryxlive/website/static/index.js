function deleteEntry(entryId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ entryIf: entryId}),
    }).then((_res) => {
        window.location.href = "/";
    });
}