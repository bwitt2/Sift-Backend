/* This file was generated by the ServiceGenerator.
 * The ServiceGenerator is Copyright (c) 2015 Google Inc.
 */

//
//  GTLSiftMainArticleRequest.h
//

// ----------------------------------------------------------------------------
// NOTE: This file is generated from Google APIs Discovery Service.
// Service:
//   sift/v1
// Description:
//   API for sift
// Classes:
//   GTLSiftMainArticleRequest (0 custom class methods, 2 custom properties)

#if GTL_BUILT_AS_FRAMEWORK
  #import "GTL/GTLObject.h"
#else
  #import "GTLObject.h"
#endif

// ----------------------------------------------------------------------------
//
//   GTLSiftMainArticleRequest
//

@interface GTLSiftMainArticleRequest : GTLObject
@property (retain) NSNumber *currentArticleTimestamp;  // longLongValue
@property (retain) NSNumber *numOfArticles;  // longLongValue
@end
