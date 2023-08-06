#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List
import minimalKNN as knn
import fdlsgm
import numpy as np


@dataclass
class Tracklet(object):
  ''' Tracklet Container

  Atrributes:
    s (ndarray):
        The starting point of the tracklet. The argument should be compatible
        with an numpy.ndarray, whose number of elements should be three.
        The array content is expectd to be (x,y,t).
    e (ndarray):
        The terminal point of the tracklet. The argument should be compatible
        with an numpy.ndarray, whose number of elements should be three.
        The array content is expectd to be (x,y,t).
    members (ndarray):
        The associated members of the tracklet. The argument should be a two-
        dimensional array compatible with an numpy.ndarray. The shape of the
        array should be (N,3), where N is the number of the members. Each
        element should have the (t,y,x)-coordinate of a vertex.
  '''
  s: np.ndarray
  e: np.ndarray
  members: np.ndarray

  def __post_init__(self):
    ''' Validation of the argument is applied here. '''
    try:
      self.s = np.array(self.s)
      assert self.s.shape == (3,)
    except Exception as e:
      raise AssertionError(
        'the starting point should have three elements.') from e
    try:
      self.e = np.array(self.e)
      assert self.e.shape == (3,)
    except Exception as e:
      raise AssertionError(
        'the terminal point should have three elements.') from e
    try:
      self.members = np.array(self.members)
      assert self.members.ndim == 2
      assert self.members.shape[1] == 3
    except Exception as e:
      raise AssertionError(
        'the shape of the members should be (N, 3).') from e


def extract(vertex: np.ndarray, *,
            n_neighbor: int=3,
            max_velocity: float=200.0,
            param: fdlsgm.solve_parameters=None):
  ''' extract tracklets from a source list.

  Parameters:
    vertex (ndarray):
        A list of extracted sources. The shape should be (N, 3), where N is the
        number of the sources. Each element should be an array of (x, y, t),
        where t is the timestamp, y and x are the location of the source.

  Return:
    A list of Tracklet instances.
  '''
  ## edges:
  ##   An ndarray with the shape of (N, 2), where N is the number of edges.
  ##   The first element is the index of the starting vertex, while the
  ##   second element is the index of the end vertex.
  edge = np.array(knn.compressed_graph(vertex, n_neighbor))
  ## return an empty list when no edge is found.
  if len(edge)==0: return list()

  ## drop edges with the same z-location.
  z,y,x = vertex[:,2],vertex[:,1],vertex[:,0]
  edge = edge[z[edge[:,0]]!=z[edge[:,1]]]
  ## return an empty list when no edge remains.
  if len(edge)==0: return list()

  ## drop edges faster than max_velocity.
  dx  = x[edge[:,0]]-x[edge[:,1]]
  dy  = y[edge[:,0]]-y[edge[:,1]]
  dz  = z[edge[:,0]]-z[edge[:,1]]
  sqv = (dx*dx+dy*dy)/(dz*dz)
  edge = edge[sqv < max_velocity**2]
  ## return an empty list when no edge remains.
  if len(edge)==0: return list()

  ## correct the direction of the edges.
  inv = z[edge[:,0]]>z[edge[:,1]]
  edge[inv,:] = edge[inv,::-1]

  ## v0: the vertices of starting points.
  ## v1: the vertices of terminal points.
  v0,v1 = vertex[edge[:,0],:],vertex[edge[:,1],:]
  ## els:
  ##   An array of elemental line segments with the shape of (N, 6), where
  ##   N is the number of ELSs. The element should be (t0,y0,x0,t1,y1,x1).
  ##   The first three elements are the vertex of the starting point, while
  ##   the second three elements are the vertex of the terminal point.
  els = np.hstack((v0,v1))

  if param is None:
    param = fdlsgm.default_parameters()

  ## baseline:
  ##   An array of baselines.
  ##   The baseline class has four attributes:
  ##     - vertex0 (starting point)
  ##     - vertex1 (terminal point)
  ##     - size (number of vertices)
  ##     - elements (indexes of associated vertex)
  baseline = fdlsgm.solve(els, param)

  return [
    Tracklet(b.vertex0,b.vertex1,vertex[np.unique(edge[b.elements,:])])
    for b in baseline]
