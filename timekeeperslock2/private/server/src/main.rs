#[macro_use]
extern crate rocket;
extern crate chrono;
extern crate constant_time_eq;
extern crate hex;
extern crate sha3;

use chrono::Utc;
use rocket::Request;
use sha3::{Digest, Sha3_256};

#[get("/")]
fn index() -> &'static str {
    "nothing interesting here ;)"
}

#[get("/<hash>")]
fn try_open(hash: &str) -> Option<&'static str> {
    let mut hash_bin = [0; 32];
    hex::decode_to_slice(hash, &mut hash_bin).ok()?;

    let mut sha3 = Sha3_256::default();

    let msg = Utc::now().format("%H%M    %d%m%y  ");
    sha3.update(&msg.to_string());

    let key = b"\x00\x5e\x93\x16\xac\x8c\xc6\xa7\x4c\x88\xd3\xa6\xd2\x03\x7e\x1d\x5d\xa0\x64\xa5\x13\xe3\x9d\x2a\xbe\x31\x42\xa2\x2b\x66\x1d\xd6";
    sha3.update(key);

    if constant_time_eq::constant_time_eq(&sha3.finalize(), &hash_bin) {
        Some("CTF-BR{iFczClX4gPiyGAoi01aZcgysi13f4rlC}")
    } else {
        Some("try again ;(")
    }
}

#[catch(404)]
fn not_found(_req: &Request) -> &'static str {
    "incorrect url format ;("
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index, try_open])
        .register("/", catchers![not_found])
}
