use serde::de::Visitor;
use serde::{Deserialize, Deserializer};
use serde_json;
use tree::BranchingNode;
use std::collections::HashMap;
use std::fmt;
use std::fmt::Formatter;
use std::fs;

use crate::tree::Node;

#[allow(unused_imports)]
#[allow(unused_assignments)]
#[derive(Deserialize, Debug)]
pub enum Message {
    Node,
    BranchingNode,
}

pub mod extraction {

    use crate::Message;
    use serde::Deserialize;

    #[derive(Deserialize)]
    pub struct Process {
        process: String,
        messaegs: Vec<Message>,
    }
}

#[derive(Deserialize, Debug)]
pub struct ParserNode {
    send_channel: Option<String>,
    receive_channel: Option<String>,
    message: Option<String>,
    statement: Option<String>,
    if_statem: Option<Vec<ParserNode>>,
    else_statem: Option<Vec<ParserNode>>,
}

pub mod tree {

    use serde::Deserialize;

    pub type Link = Option<Box<Node>>;

    #[derive(Deserialize)]
    pub struct Node {
        send_channel: String,
        receive_channel: String,
        message: String,
        statement: String,
        pub next: Link,
    }

    #[derive(Deserialize)]
    pub struct BranchingNode {
        pub left: Link,
        pub right: Link,
    }

    impl Node {
        pub fn new(
            channel_send: String,
            channel_receive: String,
            new_message: String,
            statement: String,
            is_incoming: bool,
        ) -> Self {
            Node {
                send_channel: channel_send,
                receive_channel: channel_receive,
                message: new_message,
                statement: statement,
                next: None,
            }
        }
    }
}

fn data_parser<'de, R>(
    mut deserializer: serde_json::Deserializer<R>,
) -> Result<HashMap<String, Vec<ParserNode>>, serde_json::Error>
where
    R: serde_json::de::Read<'de>,
{
    struct DataVisitor;

    impl<'de> Visitor<'de> for DataVisitor {
        type Value = HashMap<String, Vec<ParserNode>>;

        fn expecting(&self, formatter: &mut Formatter) -> fmt::Result {
            formatter.write_str("a map of strings to vectors of messages")
        }

        fn visit_map<V>(self, mut map: V) -> Result<Self::Value, V::Error>
        where
            V: serde::de::MapAccess<'de>,
        {
            let mut result: HashMap<String, Vec<ParserNode>> = HashMap::new();
            while let Some((key, value)) = map.next_entry::<String, Vec<ParserNode>>()? {
                if let Some(existing) = result.get_mut(&key) {
                    existing.extend(value);
                } else {
                    result.insert(key, value);
                }
            }
            Ok(result)
        }
    }

    let visitor = DataVisitor;
    deserializer.deserialize_map(visitor)
}

pub fn main() -> Result<(), Box<dyn std::error::Error>> {
    let json_data = fs::read_to_string("result.json")?;
    let data = serde_json::Deserializer::from_str(&json_data);
    let data: HashMap<String, Vec<ParserNode>> = data_parser(data)?;
    dbg!(data);

    let node = Node::new(
        "z".to_string(),
        "e".to_string(),
        "x32getcrs".to_string(),
        "in".to_string(),
        true,
    );
    Ok(())
}
