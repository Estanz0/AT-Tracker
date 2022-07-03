export async function getAllStops() {
    try {
        const response = await fetch('Stops/');
        return await response.json();
    } catch(error) {
        console.error(error);
        return [];
    }
}