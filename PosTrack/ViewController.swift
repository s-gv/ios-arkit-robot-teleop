//
//  ViewController.swift
//  PosTrack
//
//  Created by Sagar on 03/05/20.
//  Copyright © 2020 Tracecut. All rights reserved.
//

import UIKit
import SceneKit
import ARKit
import Network

class ViewController: UIViewController, ARSCNViewDelegate, ARSessionDelegate {

    @IBOutlet var sceneView: ARSCNView!
    var tapVal: Bool?
    var host: String?
    var connection: NWConnection?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set the view's delegate
        sceneView.delegate = self
        
        // Show statistics such as fps and timing information
        tapVal = true
        sceneView.showsStatistics = true
        
        // Create a new scene
        let scene = SCNScene(named: "art.scnassets/ship.scn")!
        
        // Set the scene to the view
        sceneView.scene = scene
        
        // Set up gestures
        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(self.tapGesture))
        
        let swipeGesture = UISwipeGestureRecognizer(target: self, action: #selector(self.swipeGesture))
        
        sceneView.addGestureRecognizer(tapGesture)
        sceneView.addGestureRecognizer(swipeGesture)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        
        // Create a session configuration
        let configuration = ARWorldTrackingConfiguration()

        // Run the view's session
        sceneView.session.run(configuration)
        
        sceneView.session.delegate = self
        
        // UDP Connection
        self.connection = NWConnection(host: "192.168.0.46", port: 8000, using: .udp)
        self.connection?.start(queue: .global())
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        
        // Pause the view's session
        sceneView.session.pause()
    }

    // MARK: - ARSCNViewDelegate
    
/*
    // Override to create and configure nodes for anchors added to the view's session.
    func renderer(_ renderer: SCNSceneRenderer, nodeFor anchor: ARAnchor) -> SCNNode? {
        let node = SCNNode()
     
        return node
    }
*/
    @objc
    func tapGesture() {
        // print("Tapped")
        tapVal = !tapVal!
        sceneView.showsStatistics = tapVal!
        
        let content = "Yoda--\(tapVal!) "
        self.connection?.send(content: content.data(using: .utf8), completion: NWConnection.SendCompletion.contentProcessed({ (NWError) in
        }))
    }
    
    @objc
    func swipeGesture() {
        print("Swipe")
        
        let ac = UIAlertController(title: "Host", message: "Enter host address (ex: 10.32.33.46:8000)", preferredStyle: .alert)
        ac.addTextField()
        
        let submitAction = UIAlertAction(title: "Submit", style: .default) { (_) in
            
            let host = ac.textFields![0]
            print(host)
            
            self.host = host.text!
            
        }
        ac.addAction(submitAction)
        
        present(ac, animated: true)
    }
    
    func session(_ session: ARSession, didFailWithError error: Error) {
        // Present an error message to the user
        
    }
    
    func session(_ session: ARSession, didUpdate frame: ARFrame) {
        let currentTransform = frame.camera.transform
        let x = currentTransform.columns.3.x
        let y = currentTransform.columns.3.y
        let z = currentTransform.columns.3.z
        print(x, y, z)
        
        let content = "\(x), \(y), \(z) \n"
        self.connection?.send(content: content.data(using: .utf8), completion: NWConnection.SendCompletion.contentProcessed({ (NWError) in
        }))
    }
    
    func sessionWasInterrupted(_ session: ARSession) {
        // Inform the user that the session has been interrupted, for example, by presenting an overlay
        
    }
    
    func sessionInterruptionEnded(_ session: ARSession) {
        // Reset tracking and/or remove existing anchors if consistent tracking is required
        
    }
}
