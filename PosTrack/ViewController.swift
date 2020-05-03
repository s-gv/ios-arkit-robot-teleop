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

class ViewController: UIViewController, ARSCNViewDelegate, ARSessionDelegate {

    @IBOutlet var sceneView: ARSCNView!
    var tapVal: Bool?
    var host: String?
    
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
        var request = URLRequest(url: URL(string: self.host ?? "http://192.168.0.46:8000/postrack")!)
        request.httpMethod = "POST"
        let postString = "Hello \(tapVal!)"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            
        }
        task.resume()
        
    }
    
    @objc
    func swipeGesture() {
        print("Swipe")
        
        let ac = UIAlertController(title: "POST address", message: "Enter POST address (ex: http://10.32.33.46:8000/postrack", preferredStyle: .alert)
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
        print(currentTransform.columns.3.x, currentTransform.columns.3.y, currentTransform.columns.3.z)
    }
    
    func sessionWasInterrupted(_ session: ARSession) {
        // Inform the user that the session has been interrupted, for example, by presenting an overlay
        
    }
    
    func sessionInterruptionEnded(_ session: ARSession) {
        // Reset tracking and/or remove existing anchors if consistent tracking is required
        
    }
}
